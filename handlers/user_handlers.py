from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bitcoinlib.wallets import Wallet
from configs import network

router = Router()


@router.message(Command('start'))
async def start_command(message: Message):
    wallet_name = f'tBTC{message.from_user.id}'
    wait_message = await message.answer('Подождите пожалуйста, соединение с сетью требует немного времени...')
    try:
        wallet = Wallet(wallet_name)
        wallet.utxos_update()
        balance = wallet.balance_update_from_serviceprovider()
        addr = wallet.addresslist()[0]
        await message.answer(f'адрес вашего кошелька:')
        await message.answer(f'{addr}')
        await message.answer(f'баланс = {balance} sat (обновляется после подтверждения транзакции в блокчейне сети)')
        await wait_message.delete()
    except Exception:
        wallet = Wallet.create(wallet_name, network=network)
        wallet.utxos_update()
        balance = wallet.balance_update_from_serviceprovider()
        addr = wallet.addresslist()[0]
        await message.answer(f'адрес вашего кошелька:')
        await message.answer(f'{addr}')
        await message.answer(f'баланс = {balance} sat (обновляется после подтверждения транзакции в блокчейне сети)')
        await wait_message.delete()


@router.message()
async def send_coins(message: Message):
    wallet_name = f'tBTC{message.from_user.id}'
    wait_message = await message.answer('Подождите пожалуйста, соединение с сетью требует немного времени...')
    try:
        wallet = Wallet(wallet_name)
        wallet.utxos_update()
        print(f'"{message.text.split()[0]}", "{message.text.split()[1]}", "{message.text.split()[2]}" "{network}"')
        tr = wallet.send_to(to_address=message.text.split()[0],
                            amount=int(message.text.split()[1]),
                            fee=int(message.text.split()[2]),
                            network=network,
                            offline=False)
        await message.answer('транзакция проведена успешно\n'
                             f'хэш транзакции: {tr}\n'
                             f'проверить статус транзакци можно на сайте https://blockstream.info/testnet/')
        await wait_message.delete()
    except Exception:
        await message.answer('Данные введены неверно либо баланс недостаточен.\n'
                             'Перепроверьте доступный для трат баланс своего адреса на сайте https://blockstream.info/testnet/.\n'
                             'Пример ввода данных (без скобок):\n'
                             f'[адрес получателя в сети {network}] [сумма в сатоши] [комиссия (рекомендуется не менее 5000)]')
        await wait_message.delete()

