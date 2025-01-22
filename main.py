import schedule
import asyncio
import os
import sys
import aioconsole
from dotenv import load_dotenv
from app.adapters.coinapi_adapter import CoinAPIAdapter
from app.adapters.email_notifier import EmailNotifier
from app.adapters.cli_adapter import CLIAdapter
from app.core.alert_service import AlertService

# Charger les variables depuis le fichier .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Création d'un verrou pour gérer les interactions utilisateur et la planification
user_input_lock = asyncio.Lock()

# Variable globale pour indiquer la fin de l'application
exit_flag = False

async def run_scheduler():
    """Exécuter le planificateur de tâches périodiques avec asyncio."""
    global exit_flag
    while not exit_flag:
        schedule.run_pending()
        await asyncio.sleep(1)

async def user_interaction(cli):
    """Gérer les interactions utilisateur sans bloquer."""
    global exit_flag
    while not exit_flag:
        # Réécrire l'invite après les notifications
        print("\nOptions:")
        print("1. Create a new alert")
        print("2. List all alerts")
        print("3. Delete an alert")
        print("4. Modify an alert")
        print("5. Exit")
        choice = await aioconsole.ainput("Enter your choice: ")

        if choice == "1":
            async with user_input_lock:
                symbol_input = await aioconsole.ainput("Enter cryptocurrency symbol (e.g., BTC): ")
                symbol = symbol_input.upper()

                condition_input = await aioconsole.ainput("Enter condition (below/above): ")
                condition = condition_input.lower()

                try:
                    value_input = await aioconsole.ainput("Enter target value (e.g., 5000): ")
                    value = float(value_input)
                except ValueError:
                    print("Invalid value. Please enter a numeric value.\n")
                    continue

                email = await aioconsole.ainput("Enter email to notify: ")
                cli.create_alert(symbol, condition, value, email)
                print("\nAlert created successfully.\n")

        elif choice == "2":
            async with user_input_lock:
                alerts = cli.list_alerts()
                if not alerts:
                    print("\nNo alerts currently available.\n")
                else:
                    print("\nCurrent alerts:")
                    for i, alert in enumerate(alerts, start=1):
                        print(f"{i}. {alert}")
                    print()

        elif choice == "3":
            async with user_input_lock:
                alerts = cli.list_alerts()
                if not alerts:
                    print("\nNo alerts to delete.\n")
                    continue

                print("\nCurrent alerts:")
                for i, alert in enumerate(alerts, start=1):
                    print(f"{i}. {alert}")
                print()

                try:
                    index_input = await aioconsole.ainput("Enter the number of the alert to delete: ")
                    index = int(index_input) - 1
                    if 0 <= index < len(alerts):
                        cli.delete_alert(index)
                        print("\nAlert deleted successfully.\n")
                    else:
                        print("\nInvalid selection. Please try again.\n")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.\n")

        elif choice == "4":
            async with user_input_lock:
                alerts = cli.list_alerts()
                if not alerts:
                    print("\nNo alerts to modify.\n")
                    continue

                print("\nCurrent alerts:")
                for i, alert in enumerate(alerts, start=1):
                    print(f"{i}. {alert}")
                print()

                try:
                    index_input = await aioconsole.ainput("Enter the number of the alert to modify: ")
                    index = int(index_input) - 1
                    if 0 <= index < len(alerts):
                        symbol_input = await aioconsole.ainput(f"Enter new cryptocurrency symbol (current: {alerts[index]['symbol']}): ")
                        symbol = symbol_input.upper() if symbol_input else alerts[index]['symbol']

                        condition_input = await aioconsole.ainput(f"Enter new condition (below/above, current: {alerts[index]['condition']}): ")
                        condition = condition_input.lower() if condition_input else alerts[index]['condition']

                        try:
                            value_input = await aioconsole.ainput(f"Enter new target value (current: {alerts[index]['value']}): ")
                            value = float(value_input) if value_input else alerts[index]['value']
                        except ValueError:
                            print("\nInvalid value. Modification cancelled.\n")
                            continue

                        email_input = await aioconsole.ainput(f"Enter new email to notify (current: {alerts[index]['email']}): ")
                        email = email_input if email_input else alerts[index]['email']

                        cli.modify_alert(index, symbol, condition, value, email)
                        print("\nAlert modified successfully.\n")
                    else:
                        print("\nInvalid selection. Please try again.\n")
                except ValueError:
                    print("\nInvalid input. Please enter a valid number.\n")

        elif choice == "5":
            async with user_input_lock:
                print("\nExiting...\n")
                exit_flag = True
                break

        else:
            async with user_input_lock:
                print("\nInvalid choice. Please try again.\n")

        # Petit délai pour éviter les conflits
        await asyncio.sleep(0.1)

async def main():
    # Initialiser et vérifier les services
    alerts = []
    price_provider = CoinAPIAdapter(API_KEY)
    notifier = EmailNotifier(SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD)
    alert_service = AlertService(alerts, price_provider, notifier)
    cli = CLIAdapter(alert_service)

    # Ajouter une alerte de test
    cli.create_alert("BTC", "above", 100000, "bastien.lerousseau@gmail.com")

    print("Crypto alert system running...")

    # Planifier une tâche récurrente
    schedule.every(1).minutes.do(cli.check_alerts)

    # Lancer les tâches principales
    await asyncio.gather(run_scheduler(), user_interaction(cli))



if __name__ == "__main__":
    asyncio.run(main())
