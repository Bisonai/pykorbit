# PyKorbit

Python wrapper for Korbit's REST/WS API

## Installation

### Development

```shell
pip install -e .
```

### Production

TODO: Setup own PyPI repository.

```shell
pip install .
```

## Requirements

To get access to private APIs, you have to define `korbit_client_id` and `korbit_client_secret` environment variables in `.env` file.

You can find template in `.env.example` file.

```shell
cp .env.example .env
```

## Documentation

### Exceptions

* `pykorbit.KorbitMessageNotAccepted`
* `pykorbit.KorbitWebsocketMessageReceiveFailed`
* `pykorbit.KorbitUnexpectedResponse`


### Methods

* `pykorbit.KorbitAuthentication`
* `pykorbit.KorbitRestPublic`
* `pykorbit.KorbitGeneral`
* `pykorbit.KorbitWallet`
* `pykorbit.KorbitWebsocket`

### `pykorbit.KorbitAuthentication`

#### `pykorbit.KorbitAuthentication.issue_access_token(client_id: str, client_secret: str) -> Dict[str, str]`

https://apidocs.korbit.co.kr/#direct-authentication

##### Response

```json
{
  "token_type":"Bearer",
  "access_token":"1t1LgTslDrGznxPxhYz7RldsNVIbnEK",
  "expires_in":3600,
  "scope": "VIEW,TRADE",
  "refresh_token":"vn5xoOf4PzckgnqjQSL9Sb3KxWJvYtm"
}
```

#### `pykorbit.KorbitAuthentication.renew_access_token(self, client_id: str, client_secret: str, refresh_token: str) -> Dict[str, str]`

https://apidocs.korbit.co.kr/#refreshing-access-token

##### Response

```json
{
  "token_type":"Bearer",
  "access_token":"IuqEWTK09eCLThRCZZSALA0oXC8EI7s",
  "expires_in":3600,
  "scope": "VIEW,TRADE",
  "refresh_token":"vn5xoOf4Pzckgn4jQSL9Sb3KxWJvYtm"
}
```

### `pykorbit.KorbitRestPublic`

#### `pykorbit.KorbitRestPublic.ticker(currency_pair: str) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#ticker

##### Response

```json
{
  "timestamp": 1389678052000,
  "last": "569000"
}
```

#### `pykorbit.KorbitRestPublic.detailed_ticker(currency_pair: str) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#detailed-ticker

##### Response

```json
{
  "timestamp": 1558590089274,
  "last": "9198500",
  "open": "9500000",
  "bid": "9192500",
  "ask": "9198000",
  "low": "9171500",
  "high": "9599000",
  "volume": "1539.18571988",
  "change": "-301500",
  "changePercent": "-3.17"
}
```

#### `pykorbit.KorbitRestPublic.orderbook(currency_pair: str) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#orderbook

##### Response

```json
{
  "timestamp" : 1386135077000,
  "bids" : [["1100000", "0.0103918", "1"], ["1000000", "0.01000000", "1"], ... ],
  "asks" : [["569000", "0.50000000", "1"], ["568500", "2.00000000", "1"], ... ]
}
```

#### `pykorbit.KorbitRestPublic.list_of_filled_orders(currency_pair: str, time: str = "hour") -> List[Dict]`

https://apidocs.korbit.co.kr/#list-of-filled-orders

##### Response

```json
[
  {
    "timestamp": 1389678052000,
    "tid": "22546",
    "price": "569000",
    "amount": "0.01000000",
    "type": "buy"
  },
  {
   "timestamp": 1389678017000,
   "tid": "22545",
   "price": "580000",
   "amount": "0.01000000",
   "type": "sell"
 }
  ...
]
```

#### `pykorbit.KorbitRestPublic.constants() -> Dict`

https://apidocs.korbit.co.kr/#constants-deprecated

DEPRECATED

#### `pykorbit.KorbitRestPublic.currency_pairs() -> List[str]`

Get all currency pairs that can be traded.

### `KorbitGeneral`

#### `pykorbit.KorbitGeneral.user_balances(access_token: str) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#user-balances

##### Response

```json
{
  "krw" : {
      "available" : "123000",
      "trade_in_use" : "13000",
      "withdrawal_in_use" : "0"
  },
  "btc" : {
      "available" : "1.50200000",
      "trade_in_use" : "0.42000000",
      "withdrawal_in_use" : "0.50280000",
      "avg_price": "7115500",
      "avg_price_updated_at": 1528944850000
  },
  ...
}
```

#### `pykorbit.KorbitGeneral.transfer_account_info(access_token: str) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#transfer-account-info

##### Response

```json
{
  "deposit": {
    "btc": {
      "address" :"3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy"
    },
    "etc": {
      "address" :"0x123f681646d4a755815f9cb19e1acc8565a0c2aa"
    },
    ...
  },
  "withdrawal": {
    ...
  }
}
```

#### `pykorbit.KorbitGeneral.trading_volume_and_fees(access_token: str, pair: List[str] = []) -> Dict[str, Any]`

https://apidocs.korbit.co.kr/#trading-volume-and-fees

##### Response

```json
{
  "eth_krw": {
    "volume" : "0",
    "maker_fee" : "0.00100000",
    "taker_fee" : "0.00200000"
  },
  ...
  "etc_krw": {
    "volume" : "6570000",
    "maker_fee" : "0.00100000",
    "taker_fee" : "0.00200000"
  },
  "total_volume" : "24140000",
  "timestamp" : 1386418990000
}
```

### `pykorbit.KorbitWallet`

https://apidocs.korbit.co.kr/#private-wallet

#### `pykorbit.KorbitWallet.view_transfers(access_token: str, currency: Optional[str] = None, type: Optional[str] = None, offset: int = 0, limit: int = 40,) -> List[Dict]`

https://apidocs.korbit.co.kr/#view-transfers

##### Response

```json
[
  {
    "id": "270",
    "type": "deposit",
    "currency": "btc",
    "amount": "0.81140000",
    "completed_at": 11750020020,
    "updated_at": 11550050080,
    "created_at": 11550020020,
    "status": "filled",
    "details": {
      "transaction_id": "2d84855aa9c...",
      "address": "1F1zAaz5x1HUXrCNLbtMDqcw6o5GNx4xqX"
  },
    ...
]
```

#### `pykorbit.KorbitWallet.query_status_of_deposit_and_withdrawal(access_token: str, currency: str, request_id: Optional[int] = None,) -> List[Dict]`

https://apidocs.korbit.co.kr/#query-status-of-deposit-and-withdrawal

##### Response

```json
[
  {
    "timestamp": 1392620446000,
    "id": "5180",
    "type": "coin-in",
    "amount": { "currency": "btc", "value": "0.01"},
    "in": "1anjg6B2XbpjHx8LFw8mXHATH54vrxs2F",
    "completedAt": 1392620446100
  }
]
```

### `pykorbit.KorbitWebsocketPublic`

Abstract class for subcribing to Korbit's channels.

### `pykorbit.KorbitWebsocketPublic.__init__(self, access_token: Optional[str] = None, logging_level: Optional[str] = None)`

#### `async pykorbit.KorbitWebsocketPublic.connect_and_subscribe_ticker(self, pairs: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.connect_and_subscribe_orderbook(self, pairs: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.connect_and_subscribe_transaction(self, pairs: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.connect_and_subscribe(self, channels: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.subscribe(self, channels: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.unsubscribe(self, channels: List[str]) -> None`

#### `async pykorbit.KorbitWebsocketPublic.receive_loop(self) -> None`

#### `async pykorbit.KorbitWebsocketPublic.receive_loop(self) -> None`

#### `async pykorbit.KorbitWebsocketPublic.worker(msg: str) -> None`

Abstract static method.
