import nmap
import subprocess
import os
import re

# Limpiar la pantalla dependiendo del sistema operativo
def limpiar_pantalla():
    sistema = os.name
    if sistema == "nt":  # Si es Windows
        subprocess.run("cls", shell=True)
    else:  # Si es Linux o Mac
        subprocess.run("clear", shell=True)

# Función para realizar el ping
def hacer_ping(ip, veces=3):
    """Realiza 3 pings a la dirección IP."""
    print(f"\nRealizando ping a {ip}...")
    sistema = os.name
    comando = []

    if sistema == "nt":  # Si es Windows
        comando = ["ping", "-n", str(veces), ip]
    else:  # Si es Linux o Mac
        comando = ["ping", "-c", str(veces), ip]

    try:
        subprocess.run(comando, check=True)
        print(f"\nPing exitoso a {ip}.")
    except subprocess.CalledProcessError:
        print(f"\nNo se pudo hacer ping a {ip}. La dirección podría no estar disponible.")

# Crear un objeto de escáner
nm = nmap.PortScanner()

def mostrar_menu():
    print("""
    ─────────────────────────────────────────────────────────────────────
    ─██████████████─██████████████████████ ██████████████─██████████████─
    ─██░░░░░░░░░░██─██████████████████████─██░░░░░░░░░░██─██░░░░░░░░░░██─
    ─██░░██████░░██─██░░░░░░░░░░░░░░░░░░██─██░░██████░░██─██░░██████░░██─
    ─██░░██──██░░██─██░░██████░░██████░░██─██░░██──██░░██─██░░██──██░░██─
    ─██░░██████░░██─██░░██──██░░██──██░░██─██░░██████░░██─██░░██████░░██─
    ─██░░░░░░░░░░██─██░░██──██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░██─
    ─██░░██████████─██░░██──██████──██░░██─██░░██████░░██─██░░██████████─
    ─██░░██─────────██░░██──────────██░░██─██░░██──██░░██─██░░██─────────
    ─██░░██─────────██░░██──────────██░░██─██░░██──██░░██─██░░██─────────
    ─██░░██─────────██░░██──────────██░░██─██░░██──██░░██─██░░██─────────
    ─██████─────────██████──────────██████─██████──██████─██████─────────
    ─────────────────────────────────────────────────────────────────────
    """)

    print("\n--- Selecciona un escaneo ---")
    print("1. Escaneo Normal (basico)")
    print("2. Escaneo Silencioso (basico +SYN)")
    print("3. Escaneo Completo (Detallado)")
    print("4. Escaneo Completo Silencioso (SYN +detallado)")
    print("5. Escaneo Completo SYN (SYN ++detallado)")
    print("6. Salir")

def realizar_escaneo(opcion, target_ip):
    """Realiza el escaneo según la opción seleccionada."""
    try:
        if opcion == 1:
            # Escaneo Normal
            print(f"\nRealizando escaneo normal en {target_ip}...")
            nm.scan(hosts=target_ip, arguments="-p 1-1024")
        elif opcion == 2:
            # Escaneo Silencioso (Escaneo TCP SYN)
            print(f"\nRealizando escaneo silencioso en {target_ip}...")
            nm.scan(hosts=target_ip, arguments="-sS -p 1-1024")
        elif opcion == 3:
            # Escaneo Completo (Con detección de versiones)
            print(f"\nRealizando escaneo completo en {target_ip}...")
            nm.scan(hosts=target_ip, arguments="-p 1-1024 -sV")  # Detección de versiones
        elif opcion == 4:
            # Escaneo Completo Silencioso (SYN + versiones)
            print(f"\nRealizando escaneo completo+ SYN en {target_ip}...")
            nm.scan(hosts=target_ip, arguments="-sS -p 1-1024 -sV")  # Detección de versiones
        elif opcion == 5:
            # Escaneo Completo SYN con todos los detalles posibles
            print(f"\nRealizando escaneo completo++ SYN en {target_ip}...")
            nm.scan(hosts=target_ip, arguments="-sS -p- -sV -O --script=default,vuln,ssl-enum-ciphers -T4")
        else:
            print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nEscaneo interrumpido por el usuario.")
    except Exception as e:
        print(f"Error al realizar el escaneo: {e}")

def mostrar_resultados(target_ip, opcion):
    """Muestra los resultados simplificados del escaneo"""
    try:
        if target_ip in nm.all_hosts():
            for host in nm.all_hosts():
                print(f"\n--- Resultados para {host} ---")
                print(f"Estado del host: {'Activo' if nm[host].state() == 'up' else 'Inactivo'}\n")
                
                # Mostrar los puertos abiertos
                print("Puertos abiertos:")
                print("-----------------------------------------------------")
                print("| Puerto  | Estado   | Servicio       | Versión    |")
                print("-----------------------------------------------------")
                for proto in nm[host].all_protocols():
                    for port in nm[host][proto].keys():
                        estado = nm[host][proto][port]['state']
                        servicio = nm[host][proto][port].get('name', 'Desconocido')
                        version = nm[host][proto][port].get('version', 'No disponible')  # Usar valor predeterminado
                        if estado == 'open':  # Mostrar solo puertos abiertos
                            print(f"| {port:<7} | {estado:<8} | {servicio:<14} | {version:<10} |")
                print("-----------------------------------------------------")

                # Mostrar el sistema operativo más probable
                if 'osmatch' in nm[host]:
                    print("\nSistema operativo más probable:")
                    # Ordenar sistemas operativos por precisión y mostrar el más probable
                    os_probable = sorted(nm[host]['osmatch'], key=lambda os: os['accuracy'], reverse=True)[0]
                    print(f"- {os_probable['name']} ({os_probable['accuracy']}% precisión)")
                else:
                    print("\nSistema operativo: No detectado.")
                
                # Mostrar los scripts de vulnerabilidades
                if 'script' in nm[host]:
                    print("\nVulnerabilidades detectadas:")
                    for script in nm[host]['script']:
                        print(f"- {script}: {nm[host]['script'][script]}")
                else:
                    print("\nNo se detectaron vulnerabilidades.")

        else:
            print(f"No se encontraron resultados para {target_ip}.")
    except Exception as e:
        print(f"Error al mostrar los resultados: {e}")

def main():
    while True:
        limpiar_pantalla()
        mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción (1-6): "))
            if opcion == 6:
                print("Saliendo del programa...")
                if os.name == "nt":  # Si es Windows
                    subprocess.run("cls", shell=True)
                else:  # Si es Linux o Mac
                    subprocess.run("clear", shell=True)
                break

            target_ip = input("Introduce la dirección IP o host a escanear: ")

            # Realizar 3 pings antes de comenzar el escaneo
            hacer_ping(target_ip, 3)

            # Realizar escaneo y permitir la interrupción con Ctrl+C
            realizar_escaneo(opcion, target_ip)
            
            # Mostrar resultados una vez que el escaneo haya terminado
            print("\nEsperando que el escaneo termine...")
            mostrar_resultados(target_ip, opcion)

            # Preguntar al usuario si desea realizar otro escaneo
            input("\nPresiona Enter para regresar al menú.")

        except ValueError:
            print("Por favor, ingresa un número válido.")
        except KeyboardInterrupt:
            print("\nEscaneo interrumpido por el usuario. Regresando al menú.")
        except Exception as e:
            print(f"Error inesperado: {e}")

# Iniciar el programa
if __name__ == "__main__":
    main()
    