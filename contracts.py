#!/usr/bin/env python3
from __future__ import annotations
from typing import Dict, Tuple, Union, Any
import decimal
import os
from functools import lru_cache

import requests
from web3 import Web3
from web3.contract import ContractFunction

import nets

T_DECODED_ETH_SIG = Tuple[ContractFunction, Dict[str, Any]]


class HarmonyEVMSmartContract:
    w3 = Web3(Web3.HTTPProvider(nets.hmy_web3))
    API_NOT_FOUND_MESSAGES = {"Not found", "contract not found"}
    ABI_API_ENDPOINT = "https://ctrver.t.hmny.io/fetchContractCode?contractAddress={0}&shard=0"
    POSSIBLE_ABIS = [
        "ERC20",
        "ERC721",
        "UniswapV2Router02",
        "USD Coin",
        "Wrapped ONE"
    ]

    @classmethod
    @lru_cache(maxsize=256)
    def lookup_harmony_smart_contract_by_address(cls, address: str, name: str = "") -> HarmonyEVMSmartContract:
        return HarmonyEVMSmartContract(address, name)

    def __init__(self, address: str, assigned_name: str):
        self.address = address
        self.name = assigned_name

        # contract function requires us to know interface of source
        self.code = HarmonyEVMSmartContract.get_code(address)
        self.has_code = not self._is_missing(self.code)
        self.abi = self.has_code and self.code['abi'] or getABI(self.POSSIBLE_ABIS[0])
        self.abi_attempt_idx = 1
        self.contract = HarmonyEVMSmartContract.w3.eth.contract( # noqa
            Web3.toChecksumAddress(self.address),
            abi=self.abi
        )

    def decode_input(self, tx_input: hex) -> Tuple[bool, Union[T_DECODED_ETH_SIG, None]]:
        if self.abi_attempt_idx > len(self.POSSIBLE_ABIS) - 1:
            # can't decode this, even after trying a few generic ABIs
            return False, None

        try:
            f = self.contract.decode_function_input(tx_input)
            return True, f
        except ValueError:
            # can't decode this input, keep shuffling different ABIs until get match, then stop
            self.abi = getABI(self.POSSIBLE_ABIS[self.abi_attempt_idx])
            self.abi_attempt_idx += 1
            return self.decode_input(tx_input)

    @staticmethod
    @lru_cache(maxsize=256)
    def get_code(address: str) -> Dict:
        url = HarmonyEVMSmartContract.get_code_request_url(address)
        return requests.get(url).json()

    @staticmethod
    def get_code_request_url(address: str) -> str:
        return HarmonyEVMSmartContract.ABI_API_ENDPOINT.format(address)

    @staticmethod
    def _is_missing(code) -> bool:
        return code.get("message") in HarmonyEVMSmartContract.API_NOT_FOUND_MESSAGES


def getABI(contractName):
    location = os.path.abspath(__file__)
    with open('{0}/abi/{1}.json'.format('/'.join(location.split('/')[0:-1]), contractName), 'r') as f:
        ABI = f.read()
    return ABI


def valueFromWei(amount, token):
    # Simple way to determine conversion, maybe change to lookup on chain later
    # w3.fromWei doesn't seem to have an 8 decimal option for BTC
    if token in ['0x3095c7557bCb296ccc6e363DE01b760bA031F2d9', '0xdc54046c0451f9269FEe1840aeC808D36015697d']:
        return amount / decimal.Decimal(100000000)
    if token in ['0x3a4EDcf3312f44EF027acfd8c21382a5259936e7', '0x576C260513204392F0eC0bc865450872025CB1cA']:  # DFKGOLD
        weiConvert = 'kwei'
    elif token in ['0x985458E523dB3d53125813eD68c274899e9DfAb4', '0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f',
                   '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664']:  # 1USDC/1USDT
        weiConvert = 'mwei'
    elif token in gold_values:
        weiConvert = 'wei'
    else:
        weiConvert = 'ether'
    return Web3.fromWei(amount, weiConvert)


def getNativeToken(_) -> str:
    return '0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a'


def getAddressName(address):
    # default to token contract if unknown ticker
    return address_map.get(address, address)


address_map = {
    '0xf390830DF829cf22c53c8840554B98eafC5dCBc2': 'anyJewel',
    '0x3405A1bd46B85c5C029483FbECf2F3E611026e45': 'anyMAI',
    '0x647dC1366Da28f8A64EB831fC8E9F05C90d1EA5a': 'anySwapFrom',
    '0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454': 'anySwapTo',
    '0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a': 'ONE',
    '0xb12c13e66AdE1F72f71834f2FC5082Db8C091358': 'wAVAX',
    '0x53BA62dDD5a9A6B6d97C7a496D7832D13A9218c4': 'rAVAX',
    '0xDA7fE71960cd1C19E1b86D6929efD36058F60a03': 'wLumen',
    '0x95CE547D730519A90dEF30d647F37D9E5359B6Ae': 'wLUNA',
    '0xFbdd194376de19a88118e84E279b977f165d01b8': 'wMATIC',
    '0x9b68BF4bF89c115c721105eaf6BD5164aFcc51E4': 'Freyala',
    '0x7BF379FcB16b4a6F648371cD72D9D443EF24168F': 'Amethyst',
    '0xD74433B187Cf0ba998Ad9Be3486B929c76815215': 'Artemis',
    '0x3cebA57a1AA15A35a4A29a9E067D4AE441dE779F': 'Babymis',
    '0xCf1709Ad76A79d5a60210F23e81cE2460542A836': 'Tranquil',
    '0xB4aA8c8e555b3A2F1BFd04234FF803C011760E59': 'xTranq',
    '0xB55106308974CEbe299A0f0505435C47b404b9a6': 'Eden',
    '0x0159ED2E06DDCD46a25E74eb8e159Ce666B28687': 'FOX',
    '0xED0B4b0F0E2c17646682fc98ACe09feB99aF3adE': 'RVRS',
    '0x17fDEdda058d43fF1615cdb72a40Ce8704C2479A': '1SUPERBID',
    '0x44aFdBe2Cb42cc18759159f7E383afb0Ca8E57aD': 'SmugDoge',
    '0xBCF532871415Bc6e3D147d777C6ad3e68E50cd92': 'PartyHat',
    '0x7ca9C1D0bb11F1b7C31ee5538D7a75aAF2d8E2FC': 'CryptoPigs',
    '0x8Eb03202275bD598AdC23678008eF88655544910': 'Radiant',
    '0x5903720f0132E8bd48530010d9b3192B25F51D8e': 'PASTA',
    '0x3E018675c0Ef63eB361b9EF4bfEa3A3294C74C7b': 'KuroShiba',
    '0xd009b07B4a65CC769379875Edc279961D710362d': 'RAIN',
    '0x1e05C8B69e4128949FcEf16811a819eF2f55D33E': 'SONIC',
    '0x224e64ec1BDce3870a6a6c777eDd450454068FEC': 'wUST',
    '0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f': '1USDT',
    '0xE176EBE47d621b984a73036B9DA5d834411ef734': 'Binance USD',
    '0xb1f6E61E1e113625593a22fa6aa94F8052bc39E0': 'bscBNB',
    '0x0aB43550A6915F9f67d0c454C2E90385E6497EaA': 'bscBUSD',
    '0x44cED87b9F1492Bf2DCf5c16004832569f7f6cBa': 'bscUSDC',
    '0x3F56e0c36d275367b8C502090EDF38289b3dEa0d': 'MAI',
    '0x6983D1E6DEf3690C4d616b13597A09e6193EA013': '1ETH',
    '0x3095c7557bCb296ccc6e363DE01b760bA031F2d9': 'wBTC',
    '0xdc54046c0451f9269FEe1840aeC808D36015697d': '1BTC',
    '0x735aBE48e8782948a37C7765ECb76b98CdE97B0F': 'Fantom',
    '0x39aB439897380eD10558666C4377fACB0322Ad48': '1FTM',
    '0x14A7B318fED66FfDcc80C1517C172c13852865De': '1AXS',
    '0xA5445d24E5dbF641f76058CD7a95b1c402Eb97b5': 'bscTLM',
    '0x2A719aF848bf365489E548BE5edbEC1D65858e59': 'Fira',
    '0x690f506C7FB8e76d61C077Ca75341a6F8AC37Ed5': 'sFira',
    '0x973f22036A0fF3A93654e7829444ec64CB37BD78': 'Tranquil ONE Staking',
    '0x22D62b19b7039333ad773b7185BB61294F3AdC19': 'stONE',
    '0x892D81221484F690C0a97d3DD18B9144A3ECDFB7': 'MAGIC',
    '0x093956649D43f23fe4E7144fb1C3Ad01586cCf1e': 'Jewel LP Token AVAX/Jewel',
    '0xEb579ddcD49A7beb3f205c9fF6006Bb6390F138f': 'Jewel LP Token ONE/Jewel',
    '0xFdAB6B23053E22b74f21ed42834D7048491F8F32': 'Jewel LP Token ONE/xJewel',
    '0x66C17f5381d7821385974783BE34c9b31f75Eb78': 'Jewel LP Token ONE/1USDC',
    '0x3733062773B24F9bAfa1e8f2e5A352976f008A95': 'Jewel LP Token XYA/Jewel',
    '0xc74eaf04777F784A7854e8950daEb27559111b85': 'Jewel LP Token XYA/ONE',
    '0x61356C852632813f3d71D57559B06cdFf70E538B': 'Jewel LP Token ONE/UST',
    '0xb91A0dFA0178500FEDC526f26A89803C387772E8': 'Jewel LP Token Jewel/UST',
    '0xf0504847fDbe0AEFaB006EA002BfC1CFe20d8985': 'Jewel LP Token ONE/1USDT',
    '0xf33ee94922326d7C1d220298Cc9428A1Fd15dAea': 'Jewel LP Token LUMEN/Jewel',
    '0xB6e9754b90b338ccB2a74fA31de48ad89f65ec5e': 'Jewel LP Token Luna/Jewel',
    '0x7f89b5F33138C89FAd4092a7C079973C95362D53': 'Jewel LP Token Fantom/Jewel',
    '0x3E81154912E5E2Cc9B10Ad123BF14aeb93aE5318': 'Jewel LP Toekn wMatic/Jewel',
    '0x751606585FcAa73bf92Cf823b7b6D8A0398a1c99': 'Jewel LP Token MIS/Jewel',
    '0x60e0d939D4b0C71918088278bCf600470A6c8f26': 'Jewel LP Token ONE/MIS',
    '0xfB1b4457f78E4A5b985118D6b96626F9874F400c': 'Jewel LP Token ONE/bMIS',
    '0xC593893ED4b5F97CB64808c640E48B18A80E61Ff': 'Jewel LP Token MIS/COINKX',
    '0xE01502Db14929b7733e7112E173C3bCF566F996E': 'Jewel LP Token BUSD/Jewel',
    '0x0AcCE15D05B4BA4dBEdFD7AFD51EA4FA1592f75E': 'Jewel LP Token wBTC/Jewel',
    '0x997f00485B238c83f7e58C2Ea1866DFD79f04A4b': 'Jewel LP Token wBTC/1ETH',
    '0x864fcd9a42a5f6e0f76BC309Ee26c8fab473FC3e': 'Jewel LP Token 1ETH/ONE',
    '0xEaB84868f6c8569E14263a5326ECd62F5328a70f': 'Jewel LP Token 1ETH/Jewel',
    '0x3a0C4D87BdE442150779d63c1c695d003184dF52': 'Jewel LP Token BUSD/ONE',
    '0xE7d0116Dd1DBBBA2EFBAd58f097D1FFbbeDc4923': 'Jewel LP Token bscBNB/Jewel',
    '0x68a73f563ba14d51f070A6ddD073177FB794190A': 'Jewel LP Token Superbid/ONE',
    '0x95f2409a44a9B989F8C5601037C513890E90cd06': 'Jewel LP Token Superbid/Jewel',
    '0xd22AfC683130B7c899b701e86e546F19bc598167': 'Jewel LP Token AME/BUSD/ONE',
    '0xbBAE29799602437364d183fBD9272968cF5F6361': 'Jewel LP Token TRANQ/BUSD/ONE',
    '0x5d7c3e1Fa36BbEEDf77A45E69759c5bfA56570b8': 'Jewel LP Token ONE/EDEN',
    '0xC4Af332a1E154B0bfa8760Cd3F974cdB538455Bf': 'Jewel LP Token ONE/PHAT',
    '0xdfc122dfbcec9cb11da72a7314E373fE32100396': 'Jewel LP Token ONE/SMUG',
    '0x7f64A21c72590497208273Dadba0814a6762685e': 'Jewel LP Token ONE/FOX',
    '0x7Be40c6Ba2Ff1e254e4277de0178EC80a8B78204': 'Jewel LP Token ONE/PASTA',
    '0xA1221A5BBEa699f507CC00bDedeA05b5d2e32Eba': 'Jewel LP Token 1USDC/Jewel',
    '0xFD3AB633de7a747cEacAfDad6575df1D737D659E': 'Jewel LP Token MIS/LUMEN',
    '0xe9425769e13d3f928C483726de841999648e9CFd': 'Jewel LP Token MIS/FOX',
    '0xfA45e64Adf9BF3caDC65b737b2B0151C750f414C': 'Jewel LP Token MIS/Tranquil',
    '0x14eC453656Ce925C969eafFcD76d62ACA2468Eb6': 'Jewel LP Token MIS/RVRS',
    '0x6F8B3C45f582d8f0794A57fa6a467C591CED9CAD': 'Jewel LP Token wBTC/ONE',
    '0xD7Ef803Ad48654016890DdA9F12d709f87C79cD9': 'Jewel LP Token ONE',
    '0xC79245BA0248Abe8a385d588C0a9D3DB261B453c': 'Jewel LP Token DFKTEARS/Jewel',
    '0xE22297CC3452aae66cEE6ED1cb437e96219c3319': 'Jewel LP Token MIS/XYA',
    '0xF8a37164E8273cB89e631A76c53af8ad55e6Af4E': 'Jewel LP Token MIS/MAGIC',
    '0xA9Ae89Fc743891a7166a884F25abaC50615C9BaD': 'Jewel LP Token AME/FOX',
    '0xD147ac7ccEdCa0F6F34238d4b3D0CB737aC0cfB2': 'Jewel LP Token 1AXS/ONE',
    '0xC9D4786b600873EF0f4CBe60474563Fe55ec2320': 'Jewel LP Token BUSD/1FTM',
    '0x882cF21E4bf43B6d5658C27e07f5b2873DBE5718': 'Jewel LP Token AME/RAIN',
    '0xD74B9b22860b52d8d6bc666Cf8E7274D76Cd596d': 'Jewel LP Token bscTLM/Jewel',
    '0xa8589d575aeD9C6dc12C860867c5348791D2D097': 'Jewel LP Token KURO/Jewel',
    '0x500afc0C82DA45C618fbBfc2F6931Bc415d334ea': 'Jewel LP Token 1MATIC/Jewel',
    '0x321EafB0aeD358966a90513290De99763946A54b': 'Jewel LP Token DFKGold/Jewel',
    '0xB270556714136049B27485f1aA8089B10F6F7f57': 'Jewel LP Token Shvas/Jewel',
    '0x3685ec75ea531424bbe67db11e07013abeb95f1e': 'LP withdraw fees?',
    '0x6574026Db45bA8d49529145080489C3da71a82DF': 'Venom LP Token ONE/UST',
    '0xF170016d63fb89e1d559e8F87a17BCC8B7CD9c00': 'Venom LP Token ONE/USDC',
    '0xA0E4f1f65e80A7aFb07cB43956DC8b91C7dBC640': 'Venom LP Token bscUSDC/1USDC',
    '0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7': 'UniswapV2Factory',
    '0x24ad62502d1C652Cc7684081169D04896aC20f30': 'UniswapV2Router02 Serendale',
    '0xf012702a5f0e54015362cBCA26a26fc90AA832a3': 'UniswapV2Router02 VenomSwap',
    '0xcEEB22Faf32FF4EAd24565225503807e41E5FE87': 'Uniswap SonicSwap',
    '0x3C8BF7e25EbfAaFb863256A4380A8a93490d8065': 'Uniswap Defira',
    '0x32253394e1C9E33C0dA3ddD54cDEff07E457A687': 'Uniswap Foxswap',
    '0x6a82A17B48EF6be278BBC56138F35d04594587E3': 'TranqFarms',
    '0x55aE07Bb8Bae1501F9aEBF35801B5699eAE63bb7': 'xTranqFarms',
    '0x34B9aa82D89AE04f0f546Ca5eC9C93eFE1288940': 'TranqOneLending',
    '0x973f22036A0fF3A93654e7829444ec64CB37BD78': 'TranqStoneLending',
    '0xd9c0D8Ad06ABE10aB29655ff98DcAAA0E059184A': 'Tranq1WBTCLending',
    '0x481721B918c698ff5f253c56684bAC8dCa84346c': 'Tranq1BTCLending',
    '0xc63AB8c72e636C9961c5e9288b697eC5F0B8E1F7': 'Tranq1ETHLending',
    '0xCa3e902eFdb2a410C952Fd3e4ac38d7DBDCB8E96': 'Tranq1USDCLending',
    '0x7af2430eFa179dB0e76257E5208bCAf2407B2468': 'Tranq1USDTLending',
    '0x49d95736FE7f1F32E3ee5deFc26c95bA22834639': 'Tranq1DAILending',
    '0xDE010f117000Ed4037de1c199b3F371FEd5B12C7': 'Tranquil stONE ONE Staking',
    '0x08De72C31eCf51dDa637624d1e767578d1914dca': 'Tranquil LP Token Fira/ONE',
    '0xB91945E55bb4Ff672aCe118179CFdF281877bf35': 'Tranquil LP Token Tranq/ONE',
    '0xE20d839e71aF41492bBB3e52Fb2C2A87A66D076a': 'FiraFarms',
    '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F': 'Jewel',
    '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F': 'xJewels',
    '0x985458E523dB3d53125813eD68c274899e9DfAb4': '1USDC',
    '0x3685Ec75Ea531424Bbe67dB11e07013ABeB95f1e': 'Banker',
    '0xe53BF78F8b99B6d356F93F41aFB9951168cca2c6': 'Vendor',
    '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892': 'AuctionHouse',
    '0x9e30BA74500a2a66E7884d623D409563A38Ef687': 'AuctionHouse2',
    '0xc390fAA4C7f66E4D62E59C231D5beD32Ff77BEf0': 'AuctionHouseCV',
    '0x090e07dfEC66a91dfC5711f1FeDe176daf887380': 'TavernBot1',
    '0xdF0Bf714e80F5e6C994F16B05b7fFcbCB83b89e9': 'HeroSale',
    '0xa2D001C829328aa06a2DB2740c05ceE1bFA3c6bb': 'SummoningPortalv0',
    '0x65DEA93f7b886c33A78c10343267DD39727778c2': 'SummoningPortal',
    '0xf4d3aE202c9Ae516f7eb1DB5afF19Bf699A5E355': 'SummoningPortal2',
    '0xBc36D18662Bb97F9e74B1EAA1B752aA7A44595A7': 'SummoningPortalCV',
    '0x0594D86b2923076a2316EaEA4E1Ca286dAA142C1': 'MeditationCircle',
    '0xD507b6b299d9FC835a0Df92f718920D13fA49B47': 'MeditationCircleCV',
    '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924': 'MasterGardener',
    '0x87CBa8F998F902f2fff990efFa1E261F35932e57': 'Alchemist',
    '0xfFB8a55676edA75954AB45a6Ce16F88b119dC511': 'Stone Carver',
    '0x77D991987ca85214f9686131C58c1ABE4C93E547': 'LandAuction',
    '0x72F860bF73ffa3FC42B97BbcF43Ae80280CFcdc3': 'PetAuctionHouse',
    '0x576C260513204392F0eC0bc865450872025CB1cA': 'PetIncubator',
    '0xeaF833A0Ae97897f6F69a728C9c17916296cecCA': 'PetTradeIn',
    '0xD5f5bE1037e457727e011ADE9Ca54d21c21a3F8A': 'Land',
    '0xa678d193fEcC677e137a00FEFb43a9ccffA53210': 'Airdrop',
    '0x8AbEbcDBF5AF9FC602814Eabf6Fbf952acF682A2': 'Airdrops',
    '0x2b12D9A2480D6Dd9F71DabAa366C87134195b679': 'Airdrop Payments Portal',
    '0x6Ca68D6Df270a047b12Ba8405ec688B5dF42D50C': 'Payment Service',
    '0x51477E2E1481BcAE1a17DdbA777931d55c980Ecf': 'Lila Donation',
    '0xa4b9A93013A5590dB92062CF58D4b0ab4F35dBfB': 'Dev Fund',
    '0x1e3B6b278BA3b340d4BE7321e9be6DfeD0121Eac': 'Old Dev Fund',
    '0x3875e5398766a29c1B28cC2068A0396cba36eF99': 'Marketing Fund',
    '0xBd1f65e7f350C614d364AEFeB2d87F829b0E465d': 'Gen0Drop',
    '0xabD4741948374b1f5DD5Dd7599AC1f85A34cAcDD': 'Profiles',
    '0xAa9a289ce0565E4D6548e63a441e7C084E6B52F6': 'SerendaleQuest',
    '0x5100Bd31b822371108A0f63DCFb6594b9919Eaf4': 'Serendale Quest',
    '0x3132c76acF2217646fB8391918D28a16bD8A8Ef4': 'Foraging Quest',
    '0xE259e8386d38467f0E7fFEdB69c3c9C935dfaeFc': 'Fishing Quest',
    '0xe4154B6E5D240507F9699C730a496790A722DF19': 'Gardening Quest',
    '0xF5Ff69f4aC4A851730668b93Fc408bC1C49Ef4CE': 'Wishing Well Quest',
    '0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154': 'Crystalvale Quest',
    '0xE92Db3bb6E4B21a8b9123e7FdAdD887133C64bb7': 'Perilous Journey',
    '0x38e76972BD173901B5E5E43BA5cB464293B80C31': 'Potion Use',
    '0xE97196f4011dc9DA0829dd8E151EcFc0f37EE3c7': 'DFKDuel',
    '0x0405f1b828C7C9462877cC70A9f266887FF55adA': 'DFK Raffle Tix',
    '0xd3f98a53fd4388B9297f6bd0D63b75a023adf7e5': 'Gold Pot',
    '0x5F753dcDf9b1AD9AabC1346614D1f4746fd6Ce5C': 'Hero',
    '0xEb9B61B145D6489Be575D3603F4a704810e143dF': 'Hero CV',
    '0x9CC714059943D5A726fAD11087Bb6d9Ab811A2E3': 'Graveyard',
    '0x909EF175d58d0e17d3Ceb005EeCF24C1E5C6F390': 'Eternal Story Page',
    '0x3a4EDcf3312f44EF027acfd8c21382a5259936e7': 'DFK Gold',
    '0x24eA0D436d3c2602fbfEfBe6a16bBc304C963D04': 'Gaia\'s Tears',
    '0x66F5BfD910cd83d3766c4B39d13730C911b2D286': 'Shvas Rune',
    '0x8F655142104478724bbC72664042EA09EBbF7B38': 'Moksha Rune',
    '0x95d02C1Dc58F05A015275eB49E107137D9Ee81Dc': 'Grey Pet Egg',
    '0x6d605303e9Ac53C59A3Da1ecE36C9660c7A71da5': 'Green Pet Egg',
    '0x9678518e04Fe02FB30b55e2D0e554E26306d0892': 'Blue Pet Egg',
    '0x3dB1fd0Ad479A46216919758144FD15A21C3e93c': 'Yellow Pet Egg',
    '0x9edb3Da18be4B03857f3d39F83e5C6AAD67bc148': 'Golden Egg',
    '0x6e1bC01Cc52D165B357c42042cF608159A2B81c1': 'Ambertaffy',
    '0x68EA4640C5ce6cC0c9A1F17B7b882cB1cBEACcd7': 'Darkweed',
    '0x600541aD6Ce0a8b5dae68f086D46361534D20E80': 'Goldvein',
    '0x043F9bd9Bb17dFc90dE3D416422695Dd8fa44486': 'Ragweed',
    '0x094243DfABfBB3E6F71814618ace53f07362a84c': 'Redleaf',
    '0x6B10Ad6E3b99090De20bF9f95F960addC35eF3E2': 'Rockroot',
    '0xCdfFe898E687E941b124dfB7d24983266492eF1d': 'SwiftThistle',
    '0x78aED65A2Cc40C7D8B0dF1554Da60b38AD351432': 'Bloater',
    '0xe4Cfee5bF05CeF3418DA74CFB89727D8E4fEE9FA': 'Ironscale',
    '0x8Bf4A0888451C6b5412bCaD3D9dA3DCf5c6CA7BE': 'Lanterneye',
    '0xc5891912718ccFFcC9732D1942cCD98d5934C2e1': 'Redgill',
    '0xb80A07e13240C31ec6dc0B5D72Af79d461dA3A70': 'Sailfish',
    '0x372CaF681353758f985597A35266f7b330a2A44D': 'Shimmerskin',
    '0x2493cfDAcc0f9c07240B5B1C4BE08c62b8eEff69': 'Silverfin',
    '0xAC5c49Ff7E813dE1947DC74bbb1720c353079ac9': 'Blue Stem',
    '0xc0214b37FCD01511E6283Af5423CF24C96BB9808': 'Milkweed',
    '0x19B9F05cdE7A61ab7aae5b0ed91aA62FF51CF881': 'Spiderfruit',
    '0x75E8D8676d774C9429FbB148b30E304b5542aC3d': 'Shvas Rune',  # Crystalvale quest items
    '0xCd2192521BD8e33559b0CA24f3260fE6A26C28e4': 'Moksha Rune',
    '0x7E121418cC5080C96d967cf6A033B0E541935097': 'Grey Pet Egg',
    '0x8D2bC53106063A37bb3DDFCa8CfC1D262a9BDCeB': 'Green Pet Egg',
    '0xa61Bac689AD6867a605633520D70C49e1dCce853': 'Blue Pet Egg',
    '0x72F860bF73ffa3FC42B97BbcF43Ae80280CFcdc3': 'Yellow Pet Egg',
    '0xf2D479DaEdE7F9e270a90615F8b1C52F3C487bC7': 'Golden Egg',
    '0xB78d5580d6D897DE60E1A942A5C1dc07Bc716943': 'Ambertaffy',
    '0x848Ac8ddC199221Be3dD4e4124c462B806B6C4Fd': 'Darkweed',
    '0x0096ffda7A8f8E00e9F8Bbd1cF082c14FA9d642e': 'Goldvein',
    '0x137995beEEec688296B0118131C1052546475fF3': 'Ragweed',
    '0x473A41e71618dD0709Ba56518256793371427d79': 'Redleaf',
    '0x60170664b52c035Fcb32CF5c9694b22b47882e5F': 'Rockroot',
    '0x97b25DE9F61BBBA2aD51F1b706D4D7C04257f33A': 'Swift-Thistle',
    '0xe7a1B580942148451E47b92e95aEB8d31B0acA37': 'Frost Drum',
    '0xBcdD90034eB73e7Aec2598ea9082d381a285f63b': 'Knaproot',
    '0x80A42Dc2909C0873294c5E359e8DF49cf21c74E4': 'Shaggy Caps',
    '0xc6030Afa09EDec1fd8e63a1dE10fC00E0146DaF3': 'Skunk Shade',
    '0x268CC8248FFB72Cd5F3e73A9a20Fa2FF40EfbA61': 'Bloater',
    '0x04B43D632F34ba4D4D72B0Dc2DC4B30402e5Cf88': 'Ironscale',
    '0xc2Ff93228441Ff4DD904c60Ecbc1CfA2886C76eB': 'Lanterneye',
    '0x68eE50dD7F1573423EE0Ed9c66Fc1A696f937e81': 'Redgill',
    '0x7f46E45f6e0361e7B9304f338404DA85CB94E33D': 'Sailfish',
    '0xd44ee492889C078934662cfeEc790883DCe245f3': 'Shimmerskin',
    '0xA7CFd21223151700FB82684Cd9c693596267375D': 'Silverfin',
    '0x3bcb9A3DaB194C6D8D44B424AF383E7Db51C82BD': 'Frost Bloater',
    '0xE7CB27ad646C49dC1671Cb9207176D864922C431': 'Speckle Tail',
    '0x60A3810a3963f23Fa70591435bbe93BF8786E202': 'King Pincer',
    '0x6513757978E89e822772c16B60AE033781A29A4F': 'Three Eyed Eel',
    '0x0776b936344DE7bd58A4738306a6c76835ce5D3F': 'Blue Stem',
    '0xA2cef1763e59198025259d76Ce8F9E60d27B17B5': 'Milkweed',
    '0x3E022D84D397F18743a90155934aBAC421D5FA4C': 'Spiderfruit',  # end Crystalvale
    '0x2789F04d22a845dC854145d3c289240517f2BcF0': 'Health Vial',
    '0x87361363A75c9A6303ce813D0B2656c34B68FF52': 'Full Health Potion',
    '0x19b020001AB0C12Ffa93e1FDeF90c7C37C8C71ef': 'Mana Vial',
    '0xDc2C698aF26Ff935cD1c50Eef3a4A933C62AF18D': 'Full Mana Potion',
    '0x959ba19508827d1ed2333B1b503Bd5ab006C710e': 'Stamina Vial',
    '0xA1f8b0E88c51a45E152934686270DDF4E3356278': 'Anti-poison Potion',
    '0x1771dEc8D9A29F30d82443dE0a69e7b6824e2F53': 'Anti-blinding Potion',
    '0x7e120334D9AFFc0982719A4eacC045F78BF41C68': 'Magic Resistance Potion',
    '0xFb03c364969a0bB572Ce62b8Cd616A7DDEb4c09A': 'Toughness Potion',
    '0x872dD1595544CE22ad1e0174449C7ECE6F0bb01b': 'Switftness Potion',
    '0x27dC6AaaD95580EdF25F8B9676f1B984e09e413d': 'Atonement Crystal',
    '0x1f3F655079b70190cb79cE5bc5AE5F19dAf2A6Cf': 'Atonement Crystal Lesser',
    '0x17f3B5240C4A71a3BBF379710f6fA66B9b51f224': 'Greater Atonement Crystal',
    '0xaB464901AFBc61bAC440a97Fa568aC42885Da58B': 'Lesser Might Crystal',
    '0xb368f69bE6eDa74700763672AEB2Ae63f3d20AE6': 'Might Crystal',
    '0xdFA5aE156AD4590A0061E9c4E8cc5bd60bc775c7': 'Greater Might Crystal',
    '0x39927A2CEE5580d63A163bc402946C7600300373': 'Lesser Finesse Crystal',
    '0xc6A58eFc320A7aFDB1cD662eaf6de10Ee17103F2': 'Finesse Crystal',
    '0xd1f789f6f8a3ee3fb94adBE3e82f43AAb51759Ee': 'Greater Finesse Crystal',
    '0xf5c26F2F34E9245C3A9ea0B0e7Ea7B33E6404Da0': 'Lesser Swiftness Crystal',
    '0x5d7f20e3B0f1406Bf038175218eA7e9B4838908c': 'Swiftness Crystal',
    '0x1e38e63227D52CBaDA2f0c11bE04feD64154ea37': 'Greater Swiftness Crystal',
    '0x0d8403E47445DB9E316E36F476dacD5827220Bdd': 'Lesser Vigor Crystal',
    '0xBbA50bD111DC586Fd1f2B1476B6eC505800A3FD0': 'Vigor Crystal',
    '0x5292dbce7eC2e10dd500984A163A5aE8abA585Ce': 'Greater Vigor Crystal',
    '0x3017609B9A59B77B708D783835B6fF94a3D9E337': 'Lesser Fortitude Crystal',
    '0x603919AEB55EB13F9CDE94274fC54ab2Bd2DecE7': 'Fortitude Crystal',
    '0xFE41BFf925eD88f688332b12746ef1Da68FD4CF2': 'Greater Fortitude Crystal',
    '0x17ff2016c9ecCFBF4Fc4DA6EF95Fe646D2c9104F': 'Lesser Wit Crystal',
    '0x3619fc2386FbBC19DDC39d29A72457e758CFAD69': 'Wit Crystal',
    '0xbaAb8dB69a2FdC0b88B2B3F6F75Fa8899680c43B': 'Greater Wit Crystal',
    '0xc63b76f710e9973b8989678eb16234CfADc8D9DB': 'Lesser Insight Crystal',
    '0x117E60775584CdfA4f414E22b075F31cC9c3207C': 'Insight Crystal',
    '0x90454DbF13846CF960abc0F583c319B06aB3F280': 'Greater Insight Crystal',
    '0x13AF184aEA970Fe79E3BB7A1B0B156B195fB1f40': 'Lesser Fortune Crystal',
    '0x6D777C64f0320d8A5b31BE0FdeB694007Fc3ed45': 'Fortune Crystal',
    '0x2bC1112337B90bF8c5b9422bC1e98193a9C3d1f4': 'Greater Fortune Crystal',
    '0xa509c34306AdF6168268A213Cc47D336630bf101': 'Lesser Chaos Crystal',
    '0x45B53E55b5c0A10fdd4fE2079a562d5702F3A033': 'Chaos Crystal',
    '0x423bbec25e4888967baeDB7B4EC5b0465Fa3B87D': 'Greater Chaos Crystal',
    '0xe4E7C0c693d8A7FC159776a993495378705464A7': 'Lesser Might Stone',
    '0x6382781FE94CAadC71027c0457c9CbEff06e204c': 'Might Stone',
    '0xE7F6ea1cE7BbEbC9F2Cf080010dd938d2D8D8B1b': 'Might Stone',
    '0x2bc05bf05E273a2276F19a8Bd6738e742A5685b3': 'Greater Might Stone',
    '0xbb5614D466b77d50DdEd994892DFe6F0ACA4eEbb': 'Lesser Finesse Stone',
    '0xD0B689Cb5DE0c15792Aa456C89D64038C1F2EedC': 'Finesse Stone',
    '0x20f10ef23Cdc11Fa55E6B3703d88f19A7B345D15': 'Greater Finesse Stone',
    '0xd9A8abC0Ce1ADC23F1c1813986c9a9C21C9e7510': 'Lesser Swiftness Stone',
    '0x08f362517aD4119d93bBCd20825c2E4119abB495': 'Swiftness Stone',
    '0xA1a56D20e4ba3fd2FB91c80f611ECa43c1311Afe': 'Greater Swiftness Stone',
    '0xB00CbF5Cd5e7b321436C2D3d8078773522D2F073': 'Lesser Vigor Stone',
    '0x9df75917aC9747B4A70fa033E4b0182d85B62857': 'Vigor Stone',
    '0x00a2E2F8Feb81FDB7205992B5Abd2a801b419394': 'Greater Vigor Stone',
    '0x1f57eb682377f5Ad6276b9315412920BdF9530f6': 'Lesser Fortitude Stone',
    '0x17Fa96ba9d9C29e4B96d29A7e89a4E7B240E3343': 'Fortitude Stone',
    '0x27AF2A00B42Dcc0084A6Dc99169efbFE98eb140C': 'Greater Fortitude Stone',
    '0x4Ff7A020ec1100D36d5C81F3D4815F2e9C704b59': 'Lesser Wit Stone',
    '0x939Ea05C81aAC48F7C10BdB08615082B82C80c63': 'Wit Stone',
    '0xa6e86F2b43Ae73cfB09A3bA779AeB8Fd48417ba0': 'Greater Wit Stone',
    '0x762b98B3758d0A5Eb95B3E4A1E2914Ce0A80D99c': 'Lesser Insight Stone',
    '0x9D71Bb9C781FC2eBdD3d6cb709438e3c71200149': 'Insight Stone',
    '0x40654Da5a038963fA9750AF352ae9d3b1da2baD0': 'Greater Insight Stone',
    '0x6D6eA1D2Dc1Df6Eaa2153f212d25Cf92d13Be628': 'Lesser Fortune Stone',
    '0x5da2EffE9857DcEcB786E13566Ff37B92e1E6862': 'Fortune Stone',
    '0x7f26CB2BBBcFCE8e5866cc02a887A591E1Adc02A': 'Greater Fortune Stone',
    '0x6D4f4bC32df561a35C05866051CbE9C92759Da29': 'Lesser Chaos Stone',
    '0x3633F956410163A98D58D2D928B38C64A488654e': 'Chaos Stone',
    '0x2fB31FF9E9945c5c1911386865cD666b2C5dfeB6': 'Greater Chaos Stone',
    '0x17f3B5240C4A71a3BBF379710f6fA66B9b51f224': 'Bounty Hero Achievement',
    '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7': 'AVAX',  # Start Avalanche list
    '0x4f60a160D8C2DDdaAfe16FCC57566dB84D674BD6': 'AVAX Jewel',
    '0xd586E7F844cEa2F87f50152665BCbc2C279D8d70': 'DAI',
    '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664': 'USDC',
    '0x49D5c2BdFfac6CE2BFdB6640F4F80f226bc10bAB': 'wETH',
    '0x60781C2586D68229fde47564546784ab3fACA982': 'PNG',
    '0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106': 'Uniswap AVAX',
    '0x1f806f7C8dED893fd3caE279191ad7Aa3798E928': 'Pangolin Farms V2',
    '0x9AA76aE9f804E7a70bA3Fb8395D0042079238E9C': 'Pangolin LP Jewel/AVAX',
    '0xd7538cABBf8605BdE1f4901B47B8D42c61DE0367': 'Pangolin LP Pangolin/AVAX',
    '0xAf41a65F786339e7911F4acDAD6BD49426F2Dc6b': 'Synapse Bridge',  # Start Crystalvale list
    '0x04b9dA42306B023f3572e106B11D82aAd9D32EBb': 'Crystal',
    '0xA11f52cd55900e7faf0daca7F2BA1DF8df30AdDd': 'xCrystalOld',
    '0x6E7185872BCDf3F7a6cBbE81356e50DAFFB002d2': 'xCrystal',
    '0xCCb93dABD71c8Dad03Fc4CE5559dC3D89F67a260': 'wJewel',
    '0x77f2656d04E158f915bC22f07B779D94c1DC47Ff': 'wxJewel',
    '0xB57B60DeBDB0b8172bb6316a9164bd3C695F133a': 'dfkAVAX',
    '0x3AD9DFE640E1A9Cc1D9B0948620820D975c3803a': 'USDC',
    '0x576C260513204392F0eC0bc865450872025CB1cA': 'DFK Gold',
    '0x58E63A9bbb2047cd9Ba7E6bB4490C238d271c278': 'Gaia\'s Tears',
    '0x79fE1fCF16Cc0F7E28b4d7B97387452E3084b6dA': 'Gaia\'s Tears',
    '0x3C351E1afdd1b1BC44e931E12D4E05D6125eaeCa': 'UniswapV2Router02 Crystalvale',
    '0x4F4f66964335D7bef23C16a62Fcd3d1E89f02959': 'Bridge to Crystalvale',
    '0xA7F9B7B0f729Dc98ae748f5505497909aFfdfa8A': 'Bridge to Serendale',
    '0x57Dec9cC7f492d6583c773e2E7ad66dcDc6940Fb': 'CrystalvaleGardener',
    '0x123165B3a30fdA3655B30cfC10135C1CA3C21bFC': 'Airdrop Crystalvale',
    '0xABABB0A2c42274D0e81417B824CABca464F5c16C': 'Crystalvale Donation',
    '0x6AC38A4C112F125eac0eBDbaDBed0BC8F4575d0d': 'Crystal LP Token Jewel/xJewel',
    '0x48658E69D741024b4686C8f7b236D3F1D291f386': 'Crystal LP Token Jewel/Crystal',
    '0xF3EabeD6Bd905e0FcD68FC3dBCd6e3A4aEE55E98': 'Crystal LP Token Jewel/AVAX',
    '0xCF329b34049033dE26e4449aeBCb41f1992724D3': 'Crystal LP Token Jewel/USDC',
    '0x9f378F48d0c1328fd0C80d7Ae544C6CadB5Ba99E': 'Crystal LP Token Crystal/AVAX',
    '0x04Dec678825b8DfD2D0d9bD83B538bE3fbDA2926': 'Crystal LP Token Crystal/USDC',
    '0xE072a18f6a8f1eD4953361972edD1Eb34f3e7c4E': 'Crystal LP Token Crystal/Tears'
}

gold_values = {
    '0x0405f1b828C7C9462877cC70A9f266887FF55adA': 0,  # Raffle tix
    '0x909EF175d58d0e17d3Ceb005EeCF24C1E5C6F390': 0,  # Eternal story page
    '0x3a4EDcf3312f44EF027acfd8c21382a5259936e7': 0,  # DFK gold
    '0x576C260513204392F0eC0bc865450872025CB1cA': 0,  # DFK gold CV
    '0x24eA0D436d3c2602fbfEfBe6a16bBc304C963D04': 0,  # Gaia's Tears
    '0x58E63A9bbb2047cd9Ba7E6bB4490C238d271c278': 0,  # Gaia's Tears CV
    '0x79fE1fCF16Cc0F7E28b4d7B97387452E3084b6dA': 0,  # Gaia's Tears CV new
    '0x66F5BfD910cd83d3766c4B39d13730C911b2D286': 0,  # Shvas Rune
    '0x8F655142104478724bbC72664042EA09EBbF7B38': 0,  # Moksha Rune
    '0x9678518e04Fe02FB30b55e2D0e554E26306d0892': 0,  # Blue Pet Egg
    '0x95d02C1Dc58F05A015275eB49E107137D9Ee81Dc': 0,  # Grey Pet Egg
    '0x6d605303e9Ac53C59A3Da1ecE36C9660c7A71da5': 0,  # Green Pet Egg
    '0x3dB1fd0Ad479A46216919758144FD15A21C3e93c': 0,  # Yellow Pet Egg
    '0x9edb3Da18be4B03857f3d39F83e5C6AAD67bc148': 50000,  # Golden Egg
    '0x6e1bC01Cc52D165B357c42042cF608159A2B81c1': 12.5,  # Ambertaffy
    '0x68EA4640C5ce6cC0c9A1F17B7b882cB1cBEACcd7': 10,  # Darkweed
    '0x600541aD6Ce0a8b5dae68f086D46361534D20E80': 100,  # Goldvein
    '0x043F9bd9Bb17dFc90dE3D416422695Dd8fa44486': 2.5,  # Ragweed
    '0x094243DfABfBB3E6F71814618ace53f07362a84c': 15,  # Redleaf
    '0x6B10Ad6E3b99090De20bF9f95F960addC35eF3E2': 5,  # Rockroot
    '0xCdfFe898E687E941b124dfB7d24983266492eF1d': 75,  # SwiftThistle
    '0x78aED65A2Cc40C7D8B0dF1554Da60b38AD351432': 2.5,  # Bloater
    '0xe4Cfee5bF05CeF3418DA74CFB89727D8E4fEE9FA': 5,  # Ironscale
    '0x8Bf4A0888451C6b5412bCaD3D9dA3DCf5c6CA7BE': 5,  # Lanterneye
    '0xc5891912718ccFFcC9732D1942cCD98d5934C2e1': 15,  # Redgill
    '0xb80A07e13240C31ec6dc0B5D72Af79d461dA3A70': 50,  # Sailfish
    '0x372CaF681353758f985597A35266f7b330a2A44D': 60,  # Shimmerscale
    '0x2493cfDAcc0f9c07240B5B1C4BE08c62b8eEff69': 100,  # Silverfin
    '0xAC5c49Ff7E813dE1947DC74bbb1720c353079ac9': 5,  # Blue Stem
    '0xc0214b37FCD01511E6283Af5423CF24C96BB9808': 12.5,  # Milkweed
    '0x19B9F05cdE7A61ab7aae5b0ed91aA62FF51CF881': 10,  # Spiderfruit
    '0x75E8D8676d774C9429FbB148b30E304b5542aC3d': 0,  # Shvas Rune Crystalvale
    '0xCd2192521BD8e33559b0CA24f3260fE6A26C28e4': 0,  # Moksha Rune CV
    '0x7E121418cC5080C96d967cf6A033B0E541935097': 0,  # Grey Pet Egg CV
    '0x8D2bC53106063A37bb3DDFCa8CfC1D262a9BDCeB': 0,  # Green Pet Egg CV
    '0xa61Bac689AD6867a605633520D70C49e1dCce853': 0,  # Blue Pet Egg CV
    '0x72F860bF73ffa3FC42B97BbcF43Ae80280CFcdc3': 0,  # Yellow Pet Egg CV
    '0xf2D479DaEdE7F9e270a90615F8b1C52F3C487bC7': 50000,  # Golden Egg CV
    '0xB78d5580d6D897DE60E1A942A5C1dc07Bc716943': 12.5,  # Ambertaffy CV
    '0x848Ac8ddC199221Be3dD4e4124c462B806B6C4Fd': 10,  # Darkweed CV
    '0x0096ffda7A8f8E00e9F8Bbd1cF082c14FA9d642e': 100,  # Goldvein CV
    '0x137995beEEec688296B0118131C1052546475fF3': 2.5,  # Ragweed CV
    '0x473A41e71618dD0709Ba56518256793371427d79': 15,  # Redleaf CV
    '0x60170664b52c035Fcb32CF5c9694b22b47882e5F': 5,  # Rockroot CV
    '0x97b25DE9F61BBBA2aD51F1b706D4D7C04257f33A': 75,  # Swift-Thistle CV
    '0xe7a1B580942148451E47b92e95aEB8d31B0acA37': 0,  # Frost Drum
    '0xBcdD90034eB73e7Aec2598ea9082d381a285f63b': 0,  # Knaproot
    '0x80A42Dc2909C0873294c5E359e8DF49cf21c74E4': 0,  # Shaggy Caps
    '0xc6030Afa09EDec1fd8e63a1dE10fC00E0146DaF3': 0,  # Skunk Shade
    '0x268CC8248FFB72Cd5F3e73A9a20Fa2FF40EfbA61': 2.5,  # Bloater CV
    '0x04B43D632F34ba4D4D72B0Dc2DC4B30402e5Cf88': 5,  # Ironscale CV
    '0xc2Ff93228441Ff4DD904c60Ecbc1CfA2886C76eB': 5,  # Lanterneye CV
    '0x68eE50dD7F1573423EE0Ed9c66Fc1A696f937e81': 15,  # Redgill CV
    '0x7f46E45f6e0361e7B9304f338404DA85CB94E33D': 50,  # Sailfish CV
    '0xd44ee492889C078934662cfeEc790883DCe245f3': 60,  # Shimmerscale CV
    '0xA7CFd21223151700FB82684Cd9c693596267375D': 100,  # Silverfin CV
    '0x3bcb9A3DaB194C6D8D44B424AF383E7Db51C82BD': 2.5,  # Frost Bloater
    '0xE7CB27ad646C49dC1671Cb9207176D864922C431': 0,  # Speckle Tail
    '0x60A3810a3963f23Fa70591435bbe93BF8786E202': 0,  # King Pincer
    '0x6513757978E89e822772c16B60AE033781A29A4F': 0,  # Three Eyed Eel
    '0x0776b936344DE7bd58A4738306a6c76835ce5D3F': 5,  # Blue Stem CV
    '0xA2cef1763e59198025259d76Ce8F9E60d27B17B5': 12.5,  # Milkweed CV
    '0x3E022D84D397F18743a90155934aBAC421D5FA4C': 10,  # Spiderfruit CV
    '0x2789F04d22a845dC854145d3c289240517f2BcF0': 0,  # Health Vial
    '0x87361363A75c9A6303ce813D0B2656c34B68FF52': 0,  # Full Health Potion
    '0x19b020001AB0C12Ffa93e1FDeF90c7C37C8C71ef': 0,  # Mana Vial
    '0xDc2C698aF26Ff935cD1c50Eef3a4A933C62AF18D': 0,  # Full Mana Potion
    '0x959ba19508827d1ed2333B1b503Bd5ab006C710e': 0,  # Stamina Vial
    '0xA1f8b0E88c51a45E152934686270DDF4E3356278': 0,  # Anti-poison Potion
    '0x1771dEc8D9A29F30d82443dE0a69e7b6824e2F53': 0,  # Anti-blinding Potion
    '0x7e120334D9AFFc0982719A4eacC045F78BF41C68': 0,  # Magic Resistance Potion
    '0xFb03c364969a0bB572Ce62b8Cd616A7DDEb4c09A': 0,  # Toughness Potion
    '0x872dD1595544CE22ad1e0174449C7ECE6F0bb01b': 0,  # Switftness Potion
    '0x27dC6AaaD95580EdF25F8B9676f1B984e09e413d': 0,  # Atonement Crystal
    '0x1f3F655079b70190cb79cE5bc5AE5F19dAf2A6Cf': 0,  # Atonement Crystal Lesser
    '0x17f3B5240C4A71a3BBF379710f6fA66B9b51f224': 0,  # Greater Atonement Crystal
    '0xaB464901AFBc61bAC440a97Fa568aC42885Da58B': 0,  # Lesser Might Crystal
    '0xdFA5aE156AD4590A0061E9c4E8cc5bd60bc775c7': 0,  # Greater Might Crystal
    '0xb368f69bE6eDa74700763672AEB2Ae63f3d20AE6': 0,  # Might Crystal
    '0xdFA5aE156AD4590A0061E9c4E8cc5bd60bc775c7': 0,  # Greater Might Crystal
    '0x39927A2CEE5580d63A163bc402946C7600300373': 0,  # Lesser Finesse Crystal
    '0xc6A58eFc320A7aFDB1cD662eaf6de10Ee17103F2': 0,  # Finesse Crystal
    '0xd1f789f6f8a3ee3fb94adBE3e82f43AAb51759Ee': 0,  # Greater Finesse Crystal
    '0xf5c26F2F34E9245C3A9ea0B0e7Ea7B33E6404Da0': 0,  # Lesser Swiftness Crystal
    '0x5d7f20e3B0f1406Bf038175218eA7e9B4838908c': 0,  # Swiftness Crystal
    '0x1e38e63227D52CBaDA2f0c11bE04feD64154ea37': 0,  # Greater Swiftness Crystal
    '0x0d8403E47445DB9E316E36F476dacD5827220Bdd': 0,  # Lesser Vigor Crystal
    '0xBbA50bD111DC586Fd1f2B1476B6eC505800A3FD0': 0,  # Vigor Crystal
    '0x5292dbce7eC2e10dd500984A163A5aE8abA585Ce': 0,  # Greater Vigor Crystal
    '0x3017609B9A59B77B708D783835B6fF94a3D9E337': 0,  # Lesser Fortitude Crystal
    '0x603919AEB55EB13F9CDE94274fC54ab2Bd2DecE7': 0,  # Fortitude Crystal
    '0xFE41BFf925eD88f688332b12746ef1Da68FD4CF2': 0,  # Greater Fortitude Crystal
    '0x17ff2016c9ecCFBF4Fc4DA6EF95Fe646D2c9104F': 0,  # Lesser Wit Crystal
    '0x3619fc2386FbBC19DDC39d29A72457e758CFAD69': 0,  # Wit Crystal
    '0xbaAb8dB69a2FdC0b88B2B3F6F75Fa8899680c43B': 0,  # Greater Wit Crystal
    '0xc63b76f710e9973b8989678eb16234CfADc8D9DB': 0,  # Lesser Insight Crystal
    '0x117E60775584CdfA4f414E22b075F31cC9c3207C': 0,  # Insight Crystal
    '0x90454DbF13846CF960abc0F583c319B06aB3F280': 0,  # Greater Insight Crystal
    '0x13AF184aEA970Fe79E3BB7A1B0B156B195fB1f40': 0,  # Lesser Fortune Crystal
    '0x6D777C64f0320d8A5b31BE0FdeB694007Fc3ed45': 0,  # Fortune Crystal
    '0x2bC1112337B90bF8c5b9422bC1e98193a9C3d1f4': 0,  # Greater Fortune Crystal
    '0xa509c34306AdF6168268A213Cc47D336630bf101': 0,  # Lesser Chaos Crystal
    '0x45B53E55b5c0A10fdd4fE2079a562d5702F3A033': 0,  # Chaos Crystal
    '0x423bbec25e4888967baeDB7B4EC5b0465Fa3B87D': 0,  # Greater Chaos Crystal
    '0xe4E7C0c693d8A7FC159776a993495378705464A7': 0,  # Lesser Might Stone
    '0x6382781FE94CAadC71027c0457c9CbEff06e204c': 0,  # Might Stone
    '0xE7F6ea1cE7BbEbC9F2Cf080010dd938d2D8D8B1b': 0,  # Might Stone
    '0x2bc05bf05E273a2276F19a8Bd6738e742A5685b3': 0,  # Greater Might Stone
    '0xbb5614D466b77d50DdEd994892DFe6F0ACA4eEbb': 0,  # Lesser Finesse Stone
    '0xD0B689Cb5DE0c15792Aa456C89D64038C1F2EedC': 0,  # Finesse Stone
    '0x20f10ef23Cdc11Fa55E6B3703d88f19A7B345D15': 0,  # Greater Finesse Stone
    '0xd9A8abC0Ce1ADC23F1c1813986c9a9C21C9e7510': 0,  # Lesser Swiftness Stone
    '0x08f362517aD4119d93bBCd20825c2E4119abB495': 0,  # Swiftness Stone
    '0xA1a56D20e4ba3fd2FB91c80f611ECa43c1311Afe': 0,  # Greater Swiftness Stone
    '0xB00CbF5Cd5e7b321436C2D3d8078773522D2F073': 0,  # Lesser Vigor Stone
    '0x9df75917aC9747B4A70fa033E4b0182d85B62857': 0,  # Vigor Stone
    '0x00a2E2F8Feb81FDB7205992B5Abd2a801b419394': 0,  # Greater Vigor Stone
    '0x1f57eb682377f5Ad6276b9315412920BdF9530f6': 0,  # Lesser Fortitude Stone
    '0x17Fa96ba9d9C29e4B96d29A7e89a4E7B240E3343': 0,  # Fortitude Stone
    '0x27AF2A00B42Dcc0084A6Dc99169efbFE98eb140C': 0,  # Greater Fortitude Stone
    '0x4Ff7A020ec1100D36d5C81F3D4815F2e9C704b59': 0,  # Lesser Wit Stone
    '0x939Ea05C81aAC48F7C10BdB08615082B82C80c63': 0,  # Wit Stone
    '0xa6e86F2b43Ae73cfB09A3bA779AeB8Fd48417ba0': 0,  # Greater Wit Stone
    '0x762b98B3758d0A5Eb95B3E4A1E2914Ce0A80D99c': 0,  # Lesser Insight Stone
    '0x9D71Bb9C781FC2eBdD3d6cb709438e3c71200149': 0,  # Insight Stone
    '0x40654Da5a038963fA9750AF352ae9d3b1da2baD0': 0,  # Greater Insight Stone
    '0x6D6eA1D2Dc1Df6Eaa2153f212d25Cf92d13Be628': 0,  # Lesser Fortune Stone
    '0x5da2EffE9857DcEcB786E13566Ff37B92e1E6862': 0,  # Fortune Stone
    '0x7f26CB2BBBcFCE8e5866cc02a887A591E1Adc02A': 0,  # Greater Fortune Stone
    '0x6D4f4bC32df561a35C05866051CbE9C92759Da29': 0,  # Lesser Chaos Stone
    '0x3633F956410163A98D58D2D928B38C64A488654e': 0,  # Chaos Stone
    '0x2fB31FF9E9945c5c1911386865cD666b2C5dfeB6': 0,  # Greater Chaos Stone
    '0x17f3B5240C4A71a3BBF379710f6fA66B9b51f224': 0  # Bounty Hero Achievement
}

CV_TOKENS = {
    '0x04b9dA42306B023f3572e106B11D82aAd9D32EBb': 'Crystal',
    '0xA11f52cd55900e7faf0daca7F2BA1DF8df30AdDd': 'xCrystalOld',
    '0x6E7185872BCDf3F7a6cBbE81356e50DAFFB002d2': 'xCrystal',
    '0xCCb93dABD71c8Dad03Fc4CE5559dC3D89F67a260': 'wJewel',
    '0x77f2656d04E158f915bC22f07B779D94c1DC47Ff': 'wxJewel',
    '0xB57B60DeBDB0b8172bb6316a9164bd3C695F133a': 'dfkAVAX',
    '0x3AD9DFE640E1A9Cc1D9B0948620820D975c3803a': 'USDC',
    '0x576C260513204392F0eC0bc865450872025CB1cA': 'DFK Gold',
    '0x58E63A9bbb2047cd9Ba7E6bB4490C238d271c278': 'Gaia\'s Tears',
    '0x79fE1fCF16Cc0F7E28b4d7B97387452E3084b6dA': 'Gaia\'s Tears',
    '0x6AC38A4C112F125eac0eBDbaDBed0BC8F4575d0d': 'Crystal LP Token Jewel/xJewel',
    '0x48658E69D741024b4686C8f7b236D3F1D291f386': 'Crystal LP Token Jewel/Crystal',
    '0xF3EabeD6Bd905e0FcD68FC3dBCd6e3A4aEE55E98': 'Crystal LP Token Jewel/AVAX',
    '0xCF329b34049033dE26e4449aeBCb41f1992724D3': 'Crystal LP Token Jewel/USDC',
    '0x9f378F48d0c1328fd0C80d7Ae544C6CadB5Ba99E': 'Crystal LP Token Crystal/AVAX',
    '0x04Dec678825b8DfD2D0d9bD83B538bE3fbDA2926': 'Crystal LP Token Crystal/USDC',
    '0xE072a18f6a8f1eD4953361972edD1Eb34f3e7c4E': 'Crystal LP Token Crystal/Tears',
    '0x75E8D8676d774C9429FbB148b30E304b5542aC3d': 'Shvas Rune',
    '0xCd2192521BD8e33559b0CA24f3260fE6A26C28e4': 'Moksha Rune',
    '0x7E121418cC5080C96d967cf6A033B0E541935097': 'Grey Pet Egg',
    '0x8D2bC53106063A37bb3DDFCa8CfC1D262a9BDCeB': 'Green Pet Egg',
    '0xa61Bac689AD6867a605633520D70C49e1dCce853': 'Blue Pet Egg',
    '0x72F860bF73ffa3FC42B97BbcF43Ae80280CFcdc3': 'Yellow Pet Egg',
    '0xf2D479DaEdE7F9e270a90615F8b1C52F3C487bC7': 'Golden Egg',
    '0xB78d5580d6D897DE60E1A942A5C1dc07Bc716943': 'Ambertaffy',
    '0x848Ac8ddC199221Be3dD4e4124c462B806B6C4Fd': 'Darkweed',
    '0x0096ffda7A8f8E00e9F8Bbd1cF082c14FA9d642e': 'Goldvein',
    '0x137995beEEec688296B0118131C1052546475fF3': 'Ragweed',
    '0x473A41e71618dD0709Ba56518256793371427d79': 'Redleaf',
    '0x60170664b52c035Fcb32CF5c9694b22b47882e5F': 'Rockroot',
    '0x97b25DE9F61BBBA2aD51F1b706D4D7C04257f33A': 'Swift-Thistle',
    '0xe7a1B580942148451E47b92e95aEB8d31B0acA37': 'Frost Drum',
    '0xBcdD90034eB73e7Aec2598ea9082d381a285f63b': 'Knaproot',
    '0x80A42Dc2909C0873294c5E359e8DF49cf21c74E4': 'Shaggy Caps',
    '0xc6030Afa09EDec1fd8e63a1dE10fC00E0146DaF3': 'Skunk Shade',
    '0x268CC8248FFB72Cd5F3e73A9a20Fa2FF40EfbA61': 'Bloater',
    '0x04B43D632F34ba4D4D72B0Dc2DC4B30402e5Cf88': 'Ironscale',
    '0xc2Ff93228441Ff4DD904c60Ecbc1CfA2886C76eB': 'Lanterneye',
    '0x68eE50dD7F1573423EE0Ed9c66Fc1A696f937e81': 'Redgill',
    '0x7f46E45f6e0361e7B9304f338404DA85CB94E33D': 'Sailfish',
    '0xd44ee492889C078934662cfeEc790883DCe245f3': 'Shimmerskin',
    '0xA7CFd21223151700FB82684Cd9c693596267375D': 'Silverfin',
    '0x3bcb9A3DaB194C6D8D44B424AF383E7Db51C82BD': 'Frost Bloater',
    '0xE7CB27ad646C49dC1671Cb9207176D864922C431': 'Speckle Tail',
    '0x60A3810a3963f23Fa70591435bbe93BF8786E202': 'King Pincer',
    '0x6513757978E89e822772c16B60AE033781A29A4F': 'Three Eyed Eel',
    '0x0776b936344DE7bd58A4738306a6c76835ce5D3F': 'Blue Stem',
    '0xA2cef1763e59198025259d76Ce8F9E60d27B17B5': 'Milkweed',
    '0x3E022D84D397F18743a90155934aBAC421D5FA4C': 'Spiderfruit'
}

RUNE_TOKENS = {
    '0x66F5BfD910cd83d3766c4B39d13730C911b2D286': 'Shvas Rune',
    '0x8F655142104478724bbC72664042EA09EBbF7B38': 'Moksha Rune',
    '0x75E8D8676d774C9429FbB148b30E304b5542aC3d': 'Shvas Rune',  # Crystalvale
    '0xCd2192521BD8e33559b0CA24f3260fE6A26C28e4': 'Moksha Rune',
}

fiatTypes = {
    'usd': ['0x985458E523dB3d53125813eD68c274899e9DfAb4', '0xE176EBE47d621b984a73036B9DA5d834411ef734',
            '0x44cED87b9F1492Bf2DCf5c16004832569f7f6cBa', '0x0aB43550A6915F9f67d0c454C2E90385E6497EaA',
            '0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f', '0x224e64ec1BDce3870a6a6c777eDd450454068FEC',
            '0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664']
}

tx_fee_targets = [
    '0x0000000000000000000000000000000000000000',
    '0x000000000000000000000000000000000000dEaD',
    '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F',
    '0xa4b9A93013A5590dB92062CF58D4b0ab4F35dBfB',
    '0x3875e5398766a29c1B28cC2068A0396cba36eF99',
    '0x79F0d0670D17a89f509Ad1c16BB6021187964A29',
    '0x5cA5bcd91929c7152ca577e8c001C9b5a185F568',
    '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F'
]

payment_wallets = [
    '0x6Ca68D6Df270a047b12Ba8405ec688B5dF42D50C',
    '0xa4b9A93013A5590dB92062CF58D4b0ab4F35dBfB',
    '0x1e3B6b278BA3b340d4BE7321e9be6DfeD0121Eac',
    '0x3875e5398766a29c1B28cC2068A0396cba36eF99',
    '0x2b12D9A2480D6Dd9F71DabAa366C87134195b679'
]

alternate_pair_through_tokens = {
    '0x9678518e04Fe02FB30b55e2D0e554E26306d0892': '0x985458E523dB3d53125813eD68c274899e9DfAb4'  # Blue Egg - 1USDC
}
