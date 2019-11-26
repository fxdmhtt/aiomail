# -*- coding: utf-8 -*-

import asyncio

async def test():
    async with SMTP('smtp.example.com', 465, 'user@example.com', 'password') as smtp:
        message = Message(
            sender=Sender('Sender', 'user@example.com'),
            receivers=Receiver('Receiver', 'user@example.com'),
            text='test',
            subject='test',
        )
        await smtp.send(message)

asyncio.get_event_loop.run_until_complete(test())
