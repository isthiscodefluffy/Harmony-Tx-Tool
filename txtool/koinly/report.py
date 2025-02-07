from typing import Optional, Union, Sequence
from datetime import timezone, datetime

from txtool.harmony import HarmonyAddress, HarmonyAPI, HarmonyToken
from txtool.harmony.constants import NATIVE_TOKEN_SYMBOL

from txtool.transactions import HarmonyEVMTransaction

from .ruleset import get_label_for_tx_and_description, is_cost, KOINLY_UNSUPPORTED_COIN_NAMES


class KoinlyReportCreator:  # pylint: disable=R0902
    _KOINLY_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z"
    _KOINLY_ROW_HEADER = [
        "Date",
        "Sent Amount",
        "Sent Currency",
        "Received Amount",
        "Received Currency",
        "Fee Amount",
        "Fee Currency",
        "Net Worth Amount",
        "Net Worth Currency",
        "Label",
        "Description",
        "TxHash",
        "Method",
        "To",
        "From",
        "Explorer URL",
        "\n",
    ]
    _KOINLY_TRACKED_CURRENCY_SYMBOLS = {
        "ONE",
        "ETH",
        "BTC",
        "USDT",
        "USDC",
        "DAI",
        "MATIC",
        "BNB",
        "SOL",
        "DOT",
        "AVAX",
        "LINK",
        "CRV",
    }
    HARMONY_LAUNCH_DATE: datetime = datetime.utcfromtimestamp(
        HarmonyAPI.get_timestamp(1)
    )

    def __init__(  # pylint: disable=R0913
            self,
            address_format: Optional[str] = HarmonyAddress.FORMAT_ONE,
            omit_tracked_fiat_prices: Optional[bool] = True,
            omit_cost: Optional[bool] = True,
            date_lb_str: Optional[str] = "",
            date_ub_str: Optional[str] = "",
            # none is unlimited
            tx_limit: Union[int, None] = None,
            fiat_type: Optional[str] = "usd",
    ):
        self.address_format: str = address_format or HarmonyAddress.FORMAT_ONE
        self.omit_tracked_fiat_prices = omit_tracked_fiat_prices
        self.omit_cost = omit_cost
        self.dt_lb = (
            self._parse_date_arg(date_lb_str)
            if date_lb_str
            else self.HARMONY_LAUNCH_DATE
        )
        self.dt_ub = (
            self._parse_date_arg(date_ub_str) if date_ub_str else datetime.utcnow()
        )

        # round to nearest second
        self.dt_lb_ts = int(self.dt_lb.timestamp())
        self.dt_ub_ts = int(self.dt_ub.timestamp())

        # mostly for testing, cap the number of tx you can generate in a report
        self.tx_limit = tx_limit

        # currency to write to CSV
        self.fiat_type = fiat_type

    def get_csv_from_transactions(self, events: Sequence[HarmonyEVMTransaction]) -> str:
        # remove out of range
        events = [x for x in events if self.timestamp_is_in_bounds(x.timestamp)]

        # remove costs
        if self.omit_cost:
            events = [x for x in events if not is_cost(x)]

        return self.get_csv_row_header() + "".join(self.to_csv_row(tx) for tx in events)

    def timestamp_is_in_bounds(self, ts: int) -> bool:
        return self.dt_lb_ts <= ts <= self.dt_ub_ts

    @staticmethod
    def _parse_date_arg(date_str: str) -> datetime:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)

    @staticmethod
    def timestamp_to_utc_datetime(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    @staticmethod
    def format_utc_ts_as_str(timestamp: int) -> str:
        return KoinlyReportCreator.timestamp_to_utc_datetime(timestamp).strftime(
            KoinlyReportCreator._KOINLY_DATE_FORMAT
        )

    def get_csv_row_header(self) -> str:
        return ",".join(self._KOINLY_ROW_HEADER)

    @staticmethod
    def currency_is_tracked(coin_symbol: str) -> bool:
        return (
                coin_symbol.upper() in KoinlyReportCreator._KOINLY_TRACKED_CURRENCY_SYMBOLS
        )

    def to_csv_row(self, tx: HarmonyEVMTransaction) -> str:
        if self.omit_tracked_fiat_prices and self.currency_is_tracked(
                tx.coin_type.universal_symbol
        ):
            fiat_value = ""
        else:
            # if 0, make it blank
            fiat_value = str(tx.get_fiat_value(self.omit_cost) or "")

        label, desc = get_label_for_tx_and_description(tx)

        return ",".join(
            (
                # time of transaction
                self.format_utc_ts_as_str(tx.timestamp),
                # token sent in this tx (outgoing)
                str(tx.sent_amount or ""),
                self.format_coin_symbol(tx.sent_currency),
                # token received in this tx (incoming)
                str(tx.got_amount or ""),
                self.format_coin_symbol(tx.got_currency),
                # gas
                # koinly splits up the tx fee into a separate transaction
                "0" if self.omit_cost else str(tx.tx_fee_in_native_token),
                NATIVE_TOKEN_SYMBOL,
                # fiat conversion, if $0, leave blank in CSV
                fiat_value or "",
                str(self.fiat_type),
                # human readable stuff
                label,
                desc,
                # transaction hash
                tx.tx_hash,
                tx.get_tx_function_signature(),
                # transfer information
                tx.to_addr.get_address_str(self.address_format),
                tx.from_addr.get_address_str(self.address_format),
                tx.explorer_url,
                "\n",
            )
        )

    def format_coin_symbol(self, currency: HarmonyToken) -> str:
        if currency:
            symbol = currency.universal_symbol
            return KOINLY_UNSUPPORTED_COIN_NAMES.get(symbol, symbol)

        # null coin
        return ""
