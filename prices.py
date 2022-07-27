#!/usr/bin/env python3
import requests
from web3 import Web3
import json
import datetime
import logging
import decimal
import contracts
import nets
from constants import DECIMAL_UNITS as decimal_units, TOKEN_MAP as token_map

today_prices = {}


def priceLookup(timestamp, token, fiatType='usd'):
    lookupDate = datetime.date.fromtimestamp(timestamp).strftime('%d-%m-%Y')
    # if token is in map, switch to gecko token name instead
    if token in token_map:
        token = token_map[token]
    # Calculate based on gold price if convertible to gold
    if token in contracts.gold_values and contracts.gold_values[token] > 0:
        return decimal.Decimal(
            getPrice('0x3a4EDcf3312f44EF027acfd8c21382a5259936e7', lookupDate, fiatType) * contracts.gold_values[token])
    else:
        return decimal.Decimal(getPrice(token, lookupDate, fiatType))


def fetchPriceData(token, date):
    """
    Use coingecko API
    """
    realDate = datetime.datetime.strptime(date, '%d-%m-%Y')
    prices = None
    # Coin Gecko only has prices from October 20th 2021 forward for JEWEL
    if (realDate > datetime.datetime.strptime('19-10-2021', '%d-%m-%Y') or token != 'defi-kingdoms') and token[
        0] != '0':
        gecko_uri = "https://api.coingecko.com/api/v3/coins/{0}/history?date={1}&localization=false".format(token, date)
        r = requests.get(gecko_uri)
        if r.status_code == 200:
            result = r.json()
            try:
                prices = result['market_data']['current_price']
                marketcap = result['market_data']['market_cap']
                volume = result['market_data']['total_volume']
            except Exception as err:
                result = "Error: failed to get prices no market data {0}".format(r.text)
                logging.error(result + '\n')
            if prices != None:
                result = prices
        else:
            result = "Error: failed to get prices - {0}".format(r.text)
            logging.error(result + '\n')
    else:
        # Lookup up price in DFK contract for some stuff
        result = fetchItemPrice(token, date)
    return result


# Get price of stuff from DFK dex contract for stuff that is not listed on CoinGecko or for coins before they were there
def fetchItemPrice(token, date):
    # last ditch effort, try to find a current price pair data with jewel and base on jewel to USD
    # logging.info('getting current price from dex.')
    if token in today_prices:
        price = today_prices[token]
    else:
        # only look at harmony
        price = getCurrentPrice(token, '0x72Cb10C6bfA5624dD07Ef608027E366bd690048F', 'harmony')

        if price >= 0:
            # db.savePriceData(
            #     datetime.datetime.now().strftime('%d-%m-%Y'),
            #     token,
            #     '{ "usd" : %s }' % price,
            #     '{ "usd" : 0.0 }',
            #     '{ "usd" : 0.0 }'
            # )
            pass

    if price >= 0:
        today_prices[token] = price
        result = json.loads('{ "usd" : %s }' % price)
    else:
        result = json.loads('{ "usd" : 0.0 }')

    return result


def getPrice(token, date, fiatType='usd'):
    prices = fetchPriceData(token, date)
    if fiatType in prices:
        return prices[fiatType]
    # print('Failed to lookup a price for {0} on {1}: {2}'.format(token, date, prices))
    return -1


# Return USD price of token based on its pair to throughToken to 1USDC
def getCurrentPrice(token, throughToken, network):
    w3 = Web3(Web3.HTTPProvider(nets.hmy_web3))
    ABI = contracts.getABI('UniswapV2Router02')
    contract = w3.eth.contract(address='0x24ad62502d1C652Cc7684081169D04896aC20f30', abi=ABI)
    addrUSDC = '0x985458E523dB3d53125813eD68c274899e9DfAb4'
    if token in contracts.alternate_pair_through_tokens:
        throughToken = contracts.alternate_pair_through_tokens[token]

    tokenDecimals = getTokenInfo(w3, token)[1]
    throughTokenDecimals = getTokenInfo(w3, throughToken)[1]

    # Sometimes 8 decimal tokens will try to get looked up, so skip those
    if tokenDecimals in decimal_units and throughTokenDecimals in decimal_units:
        tokenOne = 1 if tokenDecimals == 0 else Web3.toWei(1, decimal_units[tokenDecimals])
        throughTokenOne = Web3.toWei(1, decimal_units[throughTokenDecimals])
    else:
        return -1

    price = -1
    try:
        token0Amount = contract.functions.getAmountsOut(tokenOne, [token, throughToken]).call()
        if throughToken == addrUSDC:
            # If through token is USD, we don't need to get through token to USDC
            price = contracts.valueFromWei(token0Amount[1], throughToken)
        else:
            token1Amount = contract.functions.getAmountsOut(throughTokenOne, [throughToken, addrUSDC]).call()
            price = contracts.valueFromWei(token0Amount[1], throughToken) * contracts.valueFromWei(token1Amount[1],
                                                                                                   addrUSDC)
    except Exception as err:
        logging.error('Price lookup failed for {1}: {0}'.format(err, token))

    return price


def getTokenInfo(w3, address):
    ABI = contracts.getABI('ERC20')
    contract = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=ABI)
    try:
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        name = contract.functions.name().call()
    except Exception as err:
        print('Failed to get token info for {0}'.format(address))
        print(err)
        return ['NA', 18, 'NA']

    return [symbol, decimals, name]
