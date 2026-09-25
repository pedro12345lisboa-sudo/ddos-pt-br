import asyncio
import sys
from core.engine import AttackEngine
from utils.randomizer import Randomizer

async def main():
    print("=== DeepHat Stress Test Tool ===")
    
    # Configurações iniciais (Em um projeto real, viriam do config/settings.yaml)
    target = input("Digite a URL alvo (ex: http://127.0.0.1:8080): ")
    threads = int(input("Número de conexões simultâneas: "))
    
    engine = AttackEngine(
        target_url=target,
        concurrent_requests=threads,
        user_agents=Randomizer.get_user_agents()
    )

    try:
        await engine.start()
    except KeyboardInterrupt:
        print("\n[!] Parando teste...")
        engine.stop()
    except Exception as e:
        print(f"\n[!] Erro: {e}")

if __name__ == "__main__":
    # Ajuste do path para permitir imports locais
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    asyncio.run(main())