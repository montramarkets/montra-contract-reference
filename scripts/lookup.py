"""Resolve Montra registry entries on Elysium without signing a transaction."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

RPC = "https://rpc.montramarkets.xyz"
REGISTRY = "0xf1e2fa75422f889e565f3142bdbf60b28dce2aa7"
KEYS = (
    "factory", "router", "lens", "quoteRegistry", "protocolVault",
    "feeMarket", "routeFiller", "buybackFiller", "montra", "poolManager",
    "universalRouter", "permit2", "quoter", "gatewayRouter",
)


def rpc(method, *params):
    payload = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    ).encode()
    request = Request(RPC, payload, {"Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        body = json.load(response)
    if "error" in body:
        raise SystemExit(f"{method}: {body['error']}")
    return body["result"]


def main():
    keys = sys.argv[1:] or KEYS
    if any(key not in KEYS for key in keys):
        raise SystemExit("Valid keys: " + ", ".join(KEYS))
    if int(rpc("eth_chainId"), 16) != 99901:
        raise SystemExit("Unexpected chain ID")
    block = rpc("eth_blockNumber")

    def lookup(key):
        # get(bytes32): UTF-8 registry keys are padded on the right.
        data = "0x8eaa6ac0" + key.encode().hex().ljust(64, "0")
        word = rpc("eth_call", {"to": REGISTRY, "data": data}, block)
        if len(word) != 66 or not word.startswith("0x" + "0" * 24):
            raise SystemExit(f"Invalid address response for {key}: {word}")
        return "0x" + word[-40:].lower()

    with ThreadPoolExecutor(max_workers=6) as pool:
        addresses = dict(zip(keys, pool.map(lookup, keys)))
    print(json.dumps({
        "chainId": 99901, "block": int(block, 16),
        "registry": REGISTRY, "addresses": addresses,
    }, indent=2))


if __name__ == "__main__":
    main()
