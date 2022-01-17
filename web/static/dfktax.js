var BASE_SCRIPT_URL = '/';
var address_map = {
  '0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a': 'wONE',
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
  '0xB55106308974CEbe299A0f0505435C47b404b9a6': 'Eden',
  '0x0159ED2E06DDCD46a25E74eb8e159Ce666B28687': 'FOX',
  '0xED0B4b0F0E2c17646682fc98ACe09feB99aF3adE': 'RVRS',
  '0x17fDEdda058d43fF1615cdb72a40Ce8704C2479A': '1SUPERBID',
  '0x44aFdBe2Cb42cc18759159f7E383afb0Ca8E57aD': 'SmugDoge',
  '0xBCF532871415Bc6e3D147d777C6ad3e68E50cd92': 'PartyHat',
  '0x7ca9C1D0bb11F1b7C31ee5538D7a75aAF2d8E2FC': 'CryptoPigs',
  '0x8Eb03202275bD598AdC23678008eF88655544910': 'Radiant',
  '0x5903720f0132E8bd48530010d9b3192B25F51D8e': 'PASTA',
  '0x224e64ec1BDce3870a6a6c777eDd450454068FEC': 'wUST',
  '0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f': '1USDT',
  '0xE176EBE47d621b984a73036B9DA5d834411ef734': 'BinanceUSD',
  '0xb1f6E61E1e113625593a22fa6aa94F8052bc39E0': 'bscBNB',
  '0x0aB43550A6915F9f67d0c454C2E90385E6497EaA': 'bscBUSD',
  '0x6983D1E6DEf3690C4d616b13597A09e6193EA013': '1ETH',
  '0x3095c7557bCb296ccc6e363DE01b760bA031F2d9': 'wBTC',
  '0x735aBE48e8782948a37C7765ECb76b98CdE97B0F': 'Fantom',
  '0x093956649D43f23fe4E7144fb1C3Ad01586cCf1e': 'Jewel LP Token AVAX/Jewel',
  '0xEb579ddcD49A7beb3f205c9fF6006Bb6390F138f': 'Jewel LP Token ONE/Jewel',
  '0xFdAB6B23053E22b74f21ed42834D7048491F8F32': 'Jewel LP Token ONE/xJewel',
  '0x66C17f5381d7821385974783BE34c9b31f75Eb78': 'Jewel LP Token ONE/1USDC',
  '0x3733062773B24F9bAfa1e8f2e5A352976f008A95': 'Jewel LP Token XYA/Jewel',
  '0xc74eaf04777F784A7854e8950daEb27559111b85': 'Jewel LP Token XYA/ONE',
  '0xc74eaf04777F784A7854e8950daEb27559111b85': 'Jewel LP Token XYA/Jewel/ONE',
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
  '0x3685ec75ea531424bbe67db11e07013abeb95f1e': 'LP withdraw fees?',
  '0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7': 'UniswapV2Factory',
  '0x24ad62502d1C652Cc7684081169D04896aC20f30': 'UniswapV2Router02',
  '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F': 'JewelToken',
  '0xA9cE83507D872C5e1273E745aBcfDa849DAA654F': 'xJewels',
  '0x985458E523dB3d53125813eD68c274899e9DfAb4': 'USD Coin',
  '0x3685Ec75Ea531424Bbe67dB11e07013ABeB95f1e': 'Banker',
  '0xe53BF78F8b99B6d356F93F41aFB9951168cca2c6': 'Vendor',
  '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892': 'AuctionHouse',
  '0x65DEA93f7b886c33A78c10343267DD39727778c2': 'SummoningPortal',
  '0x0594D86b2923076a2316EaEA4E1Ca286dAA142C1': 'MeditationCircle',
  '0xDB30643c71aC9e2122cA0341ED77d09D5f99F924': 'MasterGardener',
  '0xa678d193fEcC677e137a00FEFb43a9ccffA53210': 'Airdrop',
  '0xabD4741948374b1f5DD5Dd7599AC1f85A34cAcDD': 'Profiles',
  '0x5100Bd31b822371108A0f63DCFb6594b9919Eaf4': 'Serendale Quest',
  '0x3132c76acF2217646fB8391918D28a16bD8A8Ef4': 'Foraging',
  '0xE259e8386d38467f0E7fFEdB69c3c9C935dfaeFc': 'Fishing',
  '0xF5Ff69f4aC4A851730668b93Fc408bC1C49Ef4CE': 'Wishing Well',
  '0x5F753dcDf9b1AD9AabC1346614D1f4746fd6Ce5C': 'Hero',
  '0x3a4EDcf3312f44EF027acfd8c21382a5259936e7': 'DFK Gold',
  '0x24eA0D436d3c2602fbfEfBe6a16bBc304C963D04': 'Gaia\'s Tears',
  '0x66F5BfD910cd83d3766c4B39d13730C911b2D286': 'Shvas Rune',
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
  '0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7': 'AVAX',  // Start Avalanche list
  '0x4f60a160D8C2DDdaAfe16FCC57566dB84D674BD6': 'AVAX Jewel',
  '0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106': 'Uniswap AVAX',
  '0x9AA76aE9f804E7a70bA3Fb8395D0042079238E9C': 'Pangolin LP Jewel/AVAX'
}

// Populates the transaction data that was generated into the page
function loadReport(results, contentType) {
  if (contentType == 'tax') {
    loadTaxes(results);
  } else {
    loadTransactions(results);
  }
}
function loadTaxes(results) {
  var taxResult = results.tax_records;
  if (taxResult == undefined) {
    alert('No results - ' + results);
    return
  }
  $("#mappingProgress").progressbar( "option", "value", 200);
  $("#mappingPercent").html("Loading Tax Report...");
  // Populate the main Tax Report from response
  for (var i = 0; i < taxResult.length; i++) {
    recordCategory = taxResult[i].category;
    accountedString = '';
    if ( taxResult[i].amountNotAccounted > .01 ) {
      accountedString = '<img src="' + BASE_SCRIPT_URL + 'static/images/alertred.png" style="max-width:24px;float:right; title="Only found Partial Cost Basis for this item."/>';
    }
    $('#tax_' + recordCategory + '_data').show();
    $('#tax_' + recordCategory + '_data').append(
      '<tr><td>' + taxResult[i].description + '</td>' +
      '<td>' + taxResult[i].acquiredDate + '</td>' +
      '<td>' + taxResult[i].soldDate + '</td>' +
      '<td>' + usdFormat.format(taxResult[i].proceeds) + '</td>' +
      '<td>' + usdFormat.format(taxResult[i].costs) + accountedString + '</td>' +
      '<td>' + usdFormat.format(taxResult[i].gains) + '</td></tr>'
    );
  }

  // some very small accounts may result in no tax generating records
  // switch to the transaction tab in this case as there may be something there
  if ( taxResult.length == 0 ) {
    switchView('transaction')
  }
}
function loadTransactions(results) {
  var eventResult = results.event_records;
  $("#mappingProgress").progressbar( "option", "value", 400);
  $("#mappingPercent").html("Loading Hero Events...");
  loadTavernEvents(eventResult.tavern);
  $("#mappingProgress").progressbar( "option", "value", 600);
  $("#mappingPercent").html("Loading Hero Events...");
  loadSwapEvents(eventResult.swaps);
  $("#mappingProgress").progressbar( "option", "value", 800);
  $("#mappingPercent").html("Loading Hero Events...");
  loadLiquidityEvents(eventResult.liquidity);
  $("#mappingProgress").progressbar( "option", "value", 1000);
  $("#mappingPercent").html("Loading Hero Events...");
  loadGardensEvents(eventResult.gardens);
  $("#mappingProgress").progressbar( "option", "value", 1200);
  $("#mappingPercent").html("Loading Hero Events...");
  loadBankEvents(eventResult.bank);
  $("#mappingProgress").progressbar( "option", "value", 1400);
  $("#mappingPercent").html("Loading Hero Events...");
  loadAirdropEvents(eventResult.airdrops);
  $("#mappingProgress").progressbar( "option", "value", 1600);
  $("#mappingPercent").html("Loading Hero Events...");
  loadQuestEvents(eventResult.quests);
  $("#mappingProgress").progressbar( "option", "value", 1800);
  $("#mappingPercent").html("Loading Hero Events...");
  loadWalletEvents(eventResult.wallet);
  $("#mappingProgress").progressbar( "option", "value", 2000);
  $("#mappingPercent").html("Ready!");
}

function loadTavernEvents(tavernEvents) {
  // Populate the Transaction list with Hero Data
  var tavernTotals = {}
  $('#tx_tavern_count').html(' (' + tavernEvents.length + ')');
  $("#tx_tavern_data").html('<tr><th>Block Date</th><th>Item Type</th><th>Item ID</th><th>Event</th><th>Coin</th><th>Coin Amt</th><th>USD Amount</th></tr>');
  for (var i = 0; i < tavernEvents.length; i++) {
    var eventDate = new Date(tavernEvents[i].timestamp * 1000);
    var coinCost = tavernEvents[i].coinCost;
    var fiatAmount = tavernEvents[i].fiatAmount;

    if (tavernEvents[i].coinCost['py/reduce'] != undefined) {
      coinCost = tavernEvents[i].coinCost['py/reduce'][1]['py/tuple'][0];
    }
    if (tavernEvents[i].fiatAmount['py/reduce'] != undefined) {
      fiatAmount = tavernEvents[i].fiatAmount['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_tavern_data').show();
    $('#tx_tavern_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + tavernEvents[i].itemType + '</td>' +
      '<td>' + tavernEvents[i].itemID + '</td>' +
      '<td>' + tavernEvents[i].event + '</td>' +
      '<td>' + address_map[tavernEvents[i].coinType] + '</td>' +
      '<td>' + coinCost + '</td>' +
      '<td>' + usdFormat.format(fiatAmount) + '</td></tr>'
    );

    if ( tavernEvents[i].event in tavernTotals ) {
      tavernTotals[tavernEvents[i].event] += 1;
    } else {
      tavernTotals[tavernEvents[i].event] = 1;
    }
  }
  // Add summary data for each event
  var tavernTable = '';
  for (let k in tavernTotals) {
    tavernTable = tavernTable + '<tr><td>' + k + 's</td><td>' + tavernTotals[k] + '</td></tr>';
  }
  $("#smy_tavern_data").html('<table>' + tavernTable + '</table>');
}

function loadSwapEvents(swapEvents) {
  // Populate the Transaction list with Swaps Data
  var swapTotals = {}
  $('#tx_trader_count').html(' (' + swapEvents.length + ')');
  $("#tx_trader_data").html('<tr><th>Block Date</th><th>Swap Type</th><th>Swap Amount</th><th>Receive Type</th><th>Receive Amount</th><th>Swap USD Amount</th><th>Receive USD Amount</th></tr>');
  for (var i = 0; i < swapEvents.length; i++) {
    var eventDate = new Date(swapEvents[i].timestamp * 1000);
    var fiatReceiveValue = swapEvents[i].fiatReceiveValue;
    var fiatSwapValue = swapEvents[i].fiatSwapValue;

    if (swapEvents[i].fiatReceiveValue['py/reduce'] != undefined) {
      fiatReceiveValue = swapEvents[i].fiatReceiveValue['py/reduce'][1]['py/tuple'][0];
    }
    if (swapEvents[i].fiatSwapValue['py/reduce'] != undefined) {
      fiatSwapValue = swapEvents[i].fiatSwapValue['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_trader_data').show();
    $('#tx_trader_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + address_map[swapEvents[i].swapType] + '</td>' +
      '<td>' + Number(swapEvents[i].swapAmount['py/reduce'][1]['py/tuple'][0]).toFixed(3) + '</td>' +
      '<td>' + address_map[swapEvents[i].receiveType] + '</td>' +
      '<td>' + Number(swapEvents[i].receiveAmount['py/reduce'][1]['py/tuple'][0]).toFixed(3) + '</td>' +
      '<td>' + usdFormat.format(fiatSwapValue) + '</td>' +
      '<td>' + usdFormat.format(fiatReceiveValue) + '</td></tr>'
    );

    if ( address_map[swapEvents[i].swapType] in swapTotals ) {
      swapTotals[address_map[swapEvents[i].swapType]][0] += parseInt(swapEvents[i].swapAmount['py/reduce'][1]['py/tuple'][0]);
    } else {
      swapTotals[address_map[swapEvents[i].swapType]] = [parseInt(swapEvents[i].swapAmount['py/reduce'][1]['py/tuple'][0]), 0];
    }
    if ( address_map[swapEvents[i].receiveType] in swapTotals ) {
      swapTotals[address_map[swapEvents[i].receiveType]][1] += parseInt(swapEvents[i].receiveAmount['py/reduce'][1]['py/tuple'][0]);
    } else {
      swapTotals[address_map[swapEvents[i].receiveType]] = [0, parseInt(swapEvents[i].receiveAmount['py/reduce'][1]['py/tuple'][0])];
    }
  }
  // Add summary data for each coin type swapped
  var swapTable = '<table><tr><th>Coin Type</th><th>Total In</th><th>Total Out</th></tr>';
  for (let k in swapTotals) {
    swapTable = swapTable + '<tr><td>' + k + '</td><td>' + swapTotals[k][0].toFixed(0) + '</td><td>' + swapTotals[k][1].toFixed(0) + '</td></tr>';
  }
  $("#smy_trader_data").html(swapTable + '</table>');
}

function loadLiquidityEvents(liquidityEvents) {
  // Populate the Transaction list with Liquidity Pool events
  var liquidityTotals = {};
  $('#tx_liquidity_count').html(' (' + liquidityEvents.length + ')');
  $("#tx_liquidity_data").html('<tr><th>Block Date</th><th>Pool Action</th><th>LP Tokens</th><th>Coin 1 Amount</th><th>Coin 2 Amount</th><th>Coin 1 USD Value</th><th>Coin 2 USD Value</th></tr>');
  for (var i = 0; i < liquidityEvents.length; i++) {
    var eventDate = new Date(liquidityEvents[i].timestamp * 1000);
    var coin1FiatValue = liquidityEvents[i].coin1FiatValue;
    var coin2FiatValue = liquidityEvents[i].coin2FiatValue;
    var poolName = address_map[liquidityEvents[i].coin1Type] + '/' + address_map[liquidityEvents[i].coin2Type];
    if (liquidityEvents[i].coin1FiatValue['py/reduce'] != undefined) {
      coin1FiatValue = Number(liquidityEvents[i].coin1FiatValue['py/reduce'][1]['py/tuple'][0]);
    }
    if (liquidityEvents[i].coin2FiatValue['py/reduce'] != undefined) {
      coin2FiatValue = Number(liquidityEvents[i].coin2FiatValue['py/reduce'][1]['py/tuple'][0]);
    }
    $('#tx_liquidity_data').show();
    $('#tx_liquidity_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + liquidityEvents[i].action + ' ' + poolName + '</td>' +
      '<td>' + Number(liquidityEvents[i].poolAmount['py/reduce'][1]['py/tuple'][0]).toFixed(5) + '</td>' +
      '<td>' + Number(liquidityEvents[i].coin1Amount['py/reduce'][1]['py/tuple'][0]).toFixed(3) + '</td>' +
      '<td>' + Number(liquidityEvents[i].coin2Amount['py/reduce'][1]['py/tuple'][0]).toFixed(3) + '</td>' +
      '<td>' + usdFormat.format(coin1FiatValue) + '</td>' +
      '<td>' + usdFormat.format(coin2FiatValue) + '</td></tr>'
    );
    if ( poolName in liquidityTotals ) {
      if (liquidityEvents[i].action == 'withdraw') {
        liquidityTotals[poolName][0] += (coin1FiatValue + coin2FiatValue);
      } else {
        liquidityTotals[poolName][1] += (coin1FiatValue + coin2FiatValue);
      }
    } else {
      if (liquidityEvents[i].action == 'withdraw') {
        liquidityTotals[poolName] = [coin1FiatValue + coin2FiatValue, 0];
      } else {
        liquidityTotals[poolName] = [0, coin1FiatValue + coin2FiatValue];
      }
    }
  }
  // Add summary data for each pool
  var liquidityTable = '<table><tr><th>LP</th><th>Total Out</th><th>Total In</th></tr>';
  for (let k in liquidityTotals) {
    liquidityTable = liquidityTable + '<tr><td>' + k + '</td><td>' + usdFormat.format(liquidityTotals[k][0]) + '</td><td>' + usdFormat.format(liquidityTotals[k][1]) + '</td></tr>';
  }
  $("#smy_liquidity_data").html(liquidityTable + '</table>');
}

function loadGardensEvents(gardensEvents) {
  // Populate the Transaction list with Jewel rewards events from Gardens LPs
  var gardensTotals = {};
  $('#tx_gardens_count').html(' (' + gardensEvents.length + ')');
  $("#tx_gardens_data").html('<tr><th>Block Date</th><th>Location</th><th>Reward Type</th><th>Coin Type</th><th>Coin Amount</th><th>Coin USD Value</th></tr>');
  for (var i = 0; i < gardensEvents.length; i++) {
    var eventDate = new Date(gardensEvents[i].timestamp * 1000)
    var coinAmount = gardensEvents[i].coinAmount
    var fiatValue = gardensEvents[i].fiatValue;
    if (gardensEvents[i].coinAmount['py/reduce'] != undefined) {
      coinAmount = gardensEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0];
    }
    if (gardensEvents[i].fiatValue['py/reduce'] != undefined) {
      fiatValue = gardensEvents[i].fiatValue['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_gardens_data').show();
    $('#tx_gardens_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + 'Garden Jewel Reward' + '</td>' +
      '<td>' + gardensEvents[i].event + '</td>' +
      '<td>' + address_map[gardensEvents[i].coinType] + '</td>' +
      '<td>' + Number(coinAmount).toFixed(5) + '</td>' +
      '<td>' + usdFormat.format(fiatValue) + '</td></tr>'
    );
    if ( gardensEvents[i].event in gardensTotals ) {
      gardensTotals[gardensEvents[i].event] += Number(coinAmount);
    } else {
      gardensTotals[gardensEvents[i].event] = Number(coinAmount);
    }
  }
  // Add summary data for each event
  var gardensTable = '';
  for (let k in gardensTotals) {
    gardensTable = gardensTable + '<tr><td>' + k + '</td><td>' + gardensTotals[k].toFixed(3) + '</td></tr>';
  }
  $("#smy_gardens_data").html('<table>' + gardensTable + '</table>');
}

function loadBankEvents(bankEvents) {
  // Populate the transaction list with Bank deposit/withdrawal events
  var bankTotals = {};
  $('#tx_bank_count').html(' (' + bankEvents.length + ')');
  $("#tx_bank_data").html('<tr><th>Block Date</th><th>Location</th><th>Action</th><th>xJewel Multiplier</th><th>Coin Type</th><th>Coin Amount</th><th>Coin USD Value</th></tr>');
  for (var i = 0; i < bankEvents.length; i++) {
    var eventDate = new Date(bankEvents[i].timestamp * 1000)
    $('#tx_bank_data').show();
    $('#tx_bank_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + 'Bank Transaction' + '</td>' +
      '<td>' + bankEvents[i].action + '</td>' +
      '<td>' + Number(bankEvents[i].xRate['py/reduce'][1]['py/tuple'][0]).toFixed(4) + '</td>' +
      '<td>' + address_map[bankEvents[i].coinType] + '</td>' +
      '<td>' + Number(bankEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0]).toFixed(5) + '</td>' +
      '<td>' + usdFormat.format(bankEvents[i].fiatValue['py/reduce'][1]['py/tuple'][0]) + '</td></tr>'
    );
    if ( address_map[bankEvents[i].coinType] in bankTotals ) {
      if ( bankEvents[i].action == 'withdraw' ) {
        bankTotals[address_map[bankEvents[i].coinType]][0] += Number(bankEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0]);
      } else {
        bankTotals[address_map[bankEvents[i].coinType]][1] += Number(bankEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0]);
      }
    } else {
      if ( bankEvents[i].action == 'withdraw' ) {
        bankTotals[address_map[bankEvents[i].coinType]] = [Number(bankEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0]), 0];
      } else {
        bankTotals[address_map[bankEvents[i].coinType]] = [0, Number(bankEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0])];
      }
    }
  }
  // Add summary data for each event
  var bankTable = '<table><tr><th>token</th><th>total withdraws</th><th>total deposits</th></tr>';
  for (let k in bankTotals) {
    bankTable = bankTable + '<tr><td>' + k + '</td><td>' + bankTotals[k][0].toFixed(3) + '</td><td>' + bankTotals[k][1].toFixed(3) + '</td></tr>';
  }
  $("#smy_bank_data").html(bankTable + '</table>');
}

function loadAirdropEvents(airdropEvents) {
  // Populate the transaction list with Airdrop events
  var airdropTotals = {};
  $("#tx_airdrop_data").html('<tr><th>Block Date</th><th>Location</th><th>Token Type</th><th>Token Amount</th><th>Token USD Value</th></tr>');
  $('#tx_airdrop_count').html(' (' + airdropEvents.length + ')');
  for (var i = 0; i < airdropEvents.length; i++) {
    var eventDate = new Date(airdropEvents[i].timestamp * 1000)
    var tokenAmount = airdropEvents[i].tokenAmount;
    var fiatValue = airdropEvents[i].fiatValue
    if (airdropEvents[i].tokenAmount['py/reduce'] != undefined) {
      tokenAmount = Number(airdropEvents[i].tokenAmount['py/reduce'][1]['py/tuple'][0]);
    }
    if (airdropEvents[i].fiatValue['py/reduce'] != undefined) {
      fiatValue = airdropEvents[i].fiatValue['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_airdrop_data').show();
    $('#tx_airdrop_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + 'Airdrop' + '</td>' +
      '<td>' + address_map[airdropEvents[i].tokenReceived] + '</td>' +
      '<td>' + tokenAmount + '</td>' +
      '<td>' + usdFormat.format(fiatValue) + '</td></tr>'
    );
    if ( address_map[airdropEvents[i].tokenReceived] in airdropTotals ) {
      airdropTotals[address_map[airdropEvents[i].tokenReceived]] += Number(tokenAmount);
    } else {
      airdropTotals[address_map[airdropEvents[i].tokenReceived]] = Number(tokenAmount);
    }
  }
  // Add summary data for each coin
  var airdropTable = '<table><tr><th>token</th><th>Total of Airdrops</th></tr>';
  for (let k in airdropTotals) {
    airdropTable = airdropTable + '<tr><td>' + k + '</td><td>' + airdropTotals[k].toFixed(3) + '</td></tr>';
  }
  $("#smy_airdrop_data").html(airdropTable + '</table>');
}

function loadQuestEvents(questEvents) {
  // Populate the transaction list with Quest reward receipts
  var questTotals = {};
  $('#tx_quest_count').html(' (' + questEvents.length + ')');
  $("#tx_quest_data").html('<tr><th>Block Date</th><th>Location</th><th>Reward Type</th><th>Reward Amount</th><th>Reward USD Value</th></tr>');
  for (var i = 0; i < questEvents.length; i++) {
    var eventDate = new Date(questEvents[i].timestamp * 1000)
    var rewardAmount = questEvents[i].rewardAmount;
    var fiatValue = questEvents[i].fiatValue
    if (questEvents[i].rewardAmount['py/reduce'] != undefined) {
      rewardAmount = Number(questEvents[i].rewardAmount['py/reduce'][1]['py/tuple'][0]);
    }
    if (questEvents[i].fiatValue['py/reduce'] != undefined) {
      fiatValue = questEvents[i].fiatValue['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_quest_data').show();
    $('#tx_quest_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + 'Serendale' + '</td>' +
      '<td>' + address_map[questEvents[i].rewardType] + '</td>' +
      '<td>' + rewardAmount + '</td>' +
      '<td>' + usdFormat.format(fiatValue) + '</td></tr>'
    );
    if ( address_map[questEvents[i].rewardType] in questTotals ) {
      questTotals[address_map[questEvents[i].rewardType]] += rewardAmount;
    } else {
      questTotals[address_map[questEvents[i].rewardType]] = rewardAmount;
    }
  }
  // Add summary data for each reward type
  var questTable = '<table><tr><th>Reward</th><th>total gained</th></tr>';
  for (let k in questTotals) {
    questTable = questTable + '<tr><td>' + k + '</td><td>' + questTotals[k].toFixed(3) + '</td></tr>';
  }
  $("#smy_quest_data").html(questTable + '</table>');
}

function loadWalletEvents(walletEvents) {
  // Populate the transaction list with basic wallet in/out transfers
  var walletTotals = {};
  $('#tx_wallet_count').html(' (' + walletEvents.length + ')');
  $("#tx_wallet_data").html('<tr><th>Block Date</th><th>Action</th><th>Address</th><th>Coin Type</th><th>Coin Amount</th><th>Coin USD Value</th></tr>');
  for (var i = 0; i < walletEvents.length; i++) {
    var eventDate = new Date(walletEvents[i].timestamp * 1000)
    var coinAmount = walletEvents[i].coinAmount;
    var fiatValue = walletEvents[i].fiatValue
    if (walletEvents[i].coinAmount['py/reduce'] != undefined) {
      coinAmount = Number(walletEvents[i].coinAmount['py/reduce'][1]['py/tuple'][0]);
    }
    if (walletEvents[i].fiatValue['py/reduce'] != undefined) {
      fiatValue = walletEvents[i].fiatValue['py/reduce'][1]['py/tuple'][0];
    }
    $('#tx_wallet_data').show();
    $('#tx_wallet_data').append(
      '<tr><td>' + eventDate.toUTCString() + '</td>' +
      '<td>' + walletEvents[i].action + '</td>' +
      '<td>' + walletEvents[i].address + '</td>' +
      '<td>' + address_map[walletEvents[i].coinType] + '</td>' +
      '<td>' + coinAmount + '</td>' +
      '<td>' + usdFormat.format(fiatValue) + '</td></tr>'
    );
    if ( address_map[walletEvents[i].coinType] in walletTotals ) {
      if ( walletEvents[i].action == 'withdraw' ) {
        walletTotals[address_map[walletEvents[i].coinType]][0] += coinAmount;
      } else {
        walletTotals[address_map[walletEvents[i].coinType]][1] += coinAmount;
      }
    } else {
      if ( walletEvents[i].action == 'withdraw' ) {
        walletTotals[address_map[walletEvents[i].coinType]] = [coinAmount, 0];
      } else {
        walletTotals[address_map[walletEvents[i].coinType]] = [0, coinAmount];
      }
    }
  }
  // Add summary data for each coin type
  var walletTable = '<table><tr><th>Coin Type</th><th>Total Out</th><th>Total In</th></tr>';
  for (let k in walletTotals) {
    walletTable = walletTable + '<tr><td>' + k + '</td><td>' + walletTotals[k][0].toFixed(0) + '</td><td>' + walletTotals[k][1].toFixed(0) + '</td></tr>';
  }
  $("#smy_wallet_data").html(walletTable + '</table>');
}

function getQueryVar(qsvar) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == qsvar) {
      return pair[1];
    }
  }
  return -1;
}
