# Saske Transaction Monitor

Инструмент для работы с транзакциями в сети Saske (тестнет/мейннет).

## Возможности

- Создание и отправка транзакций
- Анализ транзакций и их инструкций
- Мониторинг транзакций для конкретного адреса
- Поддержка тестнета и мейннета
- Декодирование данных инструкций

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование

```python
from saske_transaction import SaskeTransaction

# Инициализация клиента (тестнет или мейннет)
saske = SaskeTransaction(network="testnet")

# Анализ транзакции
tx_info = saske.analyze_transaction("signature_here")
print(tx_info)
```

### Создание и отправка транзакции

```python
from solana.keypair import Keypair
from solana.publickey import PublicKey

# Создание ключей
sender = Keypair()
receiver = PublicKey("RECEIVER_PUBLIC_KEY")

# Создание инструкции перевода
transfer_instruction = saske.create_transfer_instruction(
    from_pubkey=sender.public_key,
    to_pubkey=receiver,
    amount=1000000  # 0.001 SOL
)

# Создание и отправка транзакции
transaction = saske.build_transaction([transfer_instruction], sender)
result = saske.send_transaction(transaction, sender)
```

### Мониторинг транзакций

```python
def callback(tx_info):
    print(f"Новая транзакция: {tx_info['signature']}")

# Мониторинг транзакций для адреса
saske.monitor_transactions("ADDRESS_HERE", callback)
```

## Структура транзакции

Каждая транзакция в Saske содержит:
- Подписи
- Сообщение с инструкциями
- Blockhash
- Метаданные

## Безопасность

- Храните приватные ключи в безопасном месте
- Используйте переменные окружения для конфиденциальных данных
- Проверяйте все транзакции перед отправкой

## Лицензия

MIT 