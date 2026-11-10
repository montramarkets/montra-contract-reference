# Montra Contracts Reference

Community address book for Montra Markets on **Elysium mainnet** (chain ID **99901**, gas asset **HYPE**). The [official Contracts page](https://montramarkets.xyz/docs/contracts) resolves addresses from the on-chain registry. Use the addresses below as a snapshot and resolve the registry again before integrating.

## Start with the registry

[0xf1e2fa75422f889e565f3142bdbf60b28dce2aa7](https://elysiumexplore.com/address/0xf1e2fa75422f889e565f3142bdbf60b28dce2aa7)

To resolve an address, call `get(bytes32)` on the registry with the exact, case-sensitive key encoded as UTF-8 and padded on the right with zeros. For the full list of named entries below, run the read-only lookup. It requires Python 3 and uses the public Montra RPC.

```sh
python3 scripts/lookup.py
python3 scripts/lookup.py factory lens montra
```

## Registry snapshot

Read on Elysium at block **3,706,484**. See [registry-snapshot.json](registry-snapshot.json) for machine-readable values. For `universalRouter`, `permit2` and `quoter`, treat zero or the registry itself as unavailable.

### Launch and trade

| Registry key | Address | Role |
| --- | --- | --- |
| `factory` | [`0x38d3ef3a06d18fa3286fb5deafe611be725fcd15`](https://elysiumexplore.com/address/0x38d3ef3a06d18fa3286fb5deafe611be725fcd15) | Launch factory proxy |
| `router` | [`0xc6e9a8e1a99023b67067b8a3605403b8d7b3a157`](https://elysiumexplore.com/address/0xc6e9a8e1a99023b67067b8a3605403b8d7b3a157) | Single-pool swap router |
| `lens` | [`0xb4c202910c40c3a83f6c55683460790aaec487d4`](https://elysiumexplore.com/address/0xb4c202910c40c3a83f6c55683460790aaec487d4) | Read-only pool and fee views |
| `quoteRegistry` | [`0x91756e3174d58482fbe59e1162573a69519c60eb`](https://elysiumexplore.com/address/0x91756e3174d58482fbe59e1162573a69519c60eb) | Supported quote assets |

### Protocol fees and MONTRA

| Registry key | Address | Role |
| --- | --- | --- |
| `protocolVault` | [`0x775f596b9d78addc48caf7fc5316d79d2d4fa68e`](https://elysiumexplore.com/address/0x775f596b9d78addc48caf7fc5316d79d2d4fa68e) | Protocol and launch fee vault |
| `feeMarket` | [`0xdbb80c888f5653b24918711fa72c03f049289dd7`](https://elysiumexplore.com/address/0xdbb80c888f5653b24918711fa72c03f049289dd7) | Protocol fee sales |
| `routeFiller` | [`0x458657cde163dc8f6a633a6efd443a2aa4714b51`](https://elysiumexplore.com/address/0x458657cde163dc8f6a633a6efd443a2aa4714b51) | Fills sales through pools |
| `buybackFiller` | [`0xd679c6d3946887a88a43787a9a957b96dc1598e6`](https://elysiumexplore.com/address/0xd679c6d3946887a88a43787a9a957b96dc1598e6) | Fills MONTRA buyback orders |
| `montra` | [`0x063f7cc5339f92a5fd7baf3d22233044fda1f327`](https://elysiumexplore.com/address/0x063f7cc5339f92a5fd7baf3d22233044fda1f327) | Official MONTRA ERC-20 |

### Uniswap v4 and bridge

| Registry key | Address | Role |
| --- | --- | --- |
| `poolManager` | [`0xe2e105d3f7209a9da11f83ccf3e7398a753823f1`](https://elysiumexplore.com/address/0xe2e105d3f7209a9da11f83ccf3e7398a753823f1) | Uniswap v4 pool settlement |
| `universalRouter` | [`0xa13f7611115752deb2b13813bdde16a5073e4b45`](https://elysiumexplore.com/address/0xa13f7611115752deb2b13813bdde16a5073e4b45) | Multihop and exact-output swaps |
| `permit2` | [`0x000000000022d473030f116ddee9f6b43ac78ba3`](https://elysiumexplore.com/address/0x000000000022d473030f116ddee9f6b43ac78ba3) | ERC-20 approvals for Universal Router |
| `quoter` | [`0x379f556c5a748bd7cc9baf0f7a344094ac1814f5`](https://elysiumexplore.com/address/0x379f556c5a748bd7cc9baf0f7a344094ac1814f5) | Uniswap v4 swap quotes |
| `gatewayRouter` | [`0x61ebbc3a29f1970af2ce862ba9c5364832e14d17`](https://elysiumexplore.com/address/0x61ebbc3a29f1970af2ce862ba9c5364832e14d17) | Canonical bridge token lookup |

## Hooks, implementation contracts and multisigs

| Entry | Address shown in supplied docs screenshot | How to confirm |
| --- | --- | --- |
| Launch hook | [`0x6b1216A40B65c83e9c9e18a562C446697B8cf8EC`](https://elysiumexplore.com/address/0x6b1216a40b65c83e9c9e18a562c446697b8cf8ec) | Read `registry.hooks()`. To verify a pool, check its own hook with `registry.isKnownHook(poolHook)`. |
| Token master | [`0x10B0292Fb853966d3039D80BbEF98B1A9507F55F`](https://elysiumexplore.com/address/0x10b0292fb853966d3039d80bbef98b1a9507f55f) | Read `factory.getModuleSet(moduleSetId)` and inspect the token implementation. |
| Splitter master | [`0x02590b55416E03FE7a3413b4e8A6BbD7E9326A6B`](https://elysiumexplore.com/address/0x02590b55416e03fe7a3413b4e8a6bbd7e9326a6b) | Read the splitter implementation from the same module set. |
| Governor Safe | Live lookup | Read `registry.owner()`. |
| Treasury Safe | Live lookup | Resolve `protocolVault`, then read its `laneAt(0)` and inspect the recipient. |

For a launch configuration, read `factory.getConfig(configId)` first and use its `moduleSetId`. An implementation address identifies a template used by clones. To inspect a launched token or its fee splitter, use the deployed instance address.

## Sources

- [Contracts](https://montramarkets.xyz/docs/contracts)
- [Build guide](https://montramarkets.xyz/docs/build)
- [Official ABI bundle](https://montramarkets.xyz/docs/abis.json)
- [Montra RPC](https://montramarkets.xyz/docs/rpc)
- [Public configuration API](https://api.montramarkets.xyz/api/config)
