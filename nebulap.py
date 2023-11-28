######################################################################################################
#SCRIPT PER LA CREAZIONE E CONFIGURAZIONE DI UNA RETE NEBULA CON LA GESTIONE DEI DOMINI DI SICUREZZA #
# Giuseppe Pio Salcuni                                                                               #
# Manuel Placella                                                                                    #
######################################################################################################

import os
import subprocess
import yaml

def get_user_input(prompt):
    return input(f"{prompt}: ")

def generate_organization_ca(org_name):
    # Creo una directory per l'organizzazione
    org_dir = f"./{org_name}_certs"
    os.makedirs(org_dir, exist_ok=True)

    # Creo l'organizzazione CA
    subprocess.run(["nebula-cert", "ca", "-name", f"{org_name}"], cwd=org_dir)

    print(f"CA per {org_name} generata con successo in {org_dir}")

def generate_certificates(org_name, name, ip, security_domains):
    # Uso la directory dell'organizzazione per i certificati
    org_dir = f"./{org_name}_certs"

    # Verifica se il nome è un dominio di sicurezza o un gruppo normale
    is_security_domain = name.startswith("sd_")

    # Se è un dominio di sicurezza, imposto il flag appropriato
    if is_security_domain:
        security_domain_flag = "--security-domain"
    else:
        security_domain_flag = "--groups"

    # Genero il certificato dell'host firmato dall'organizzazione CA
    subprocess.run(["nebula-cert", "sign", "-name", name, "-ip", ip, security_domain_flag, security_domains], cwd=org_dir)

    print(f"Certificati per {name} nell'organizzazione {org_name} generati con successo in {org_dir}")

def generate_config(org_name, name, ip, realip, security_domains, is_lighthouse=False):
    # Uso la directory dell'organizzazione per inserire le configurazioni
    org_dir = f"./{org_name}_certs"
    
    # Modifico i parametri per ogni configurazione in base al tipo di client e lighthouse
    ip_without_subnet = ip.split('/')[0]
    port_value = 4242 if is_lighthouse else 0
    
    config = {
        "pki": {
            "ca": f"{org_dir}/ca.crt",
            "cert": f"{org_dir}/{name}.crt",
            "key": f"{org_dir}/{name}.key",
        },
        "static_host_map": {
            ip_without_subnet: [f"{realip}:4242"],
        },
        "lighthouse": {
            "am_lighthouse": is_lighthouse,
            "hosts": [ip_without_subnet],
        },
        "listen": {
            "host": "0.0.0.0",
            "port": port_value,
        },
        "firewall": {
            "outbound_action": "drop",
            "inbound_action": "drop",
            "conntrack": [{"tcp_timeout": "12ms", "udp_timeout": "3m", "default_timeout": "10m"}],
            "outbound": [{"port": "any", "proto": "any", "host": "any", "groups": security_domains}],
            "inbound": [{"port": "any", "proto": "icmp", "host": "any", "groups": security_domains}],
        },
    }

    # Scrivo su file la configurazione in formato YAML
    config_file_path = f"{org_dir}/{name}_config.yml"
    with open(config_file_path, "w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

    print(f"File di configurazione per {name} nell'organizzazione {org_name} generato con successo: {config_file_path}")

def check_security_domain_overlap(resources):
    allowed_connections = set()

    for i, resource1 in enumerate(resources):
        for j, resource2 in enumerate(resources):
            if i != j:
                common_domains1_to_2 = set(resource1["security_domains"]) & set(resource2["security_domains"])
                common_domains2_to_1 = set(resource2["security_domains"]) & set(resource1["security_domains"])

                if common_domains1_to_2 and common_domains2_to_1:
                    connection = tuple(sorted([resource1['name'], resource2['name']]))
                    allowed_connections.add(connection)

    if not allowed_connections:
        print("Nessuna connessione consentita tra le risorse. Uscita...")
    else:
        print("Connessioni consentite:")
        for connection in allowed_connections:
            print(f"Connessione consentita tra {connection[0]} e {connection[1]}")


if __name__ == "__main__":
    org_name = get_user_input("Inserisci il nome dell'organizzazione")
    generate_organization_ca(org_name)

    lighthouse_name = get_user_input("Inserisci il nome del lighthouse")
    lighthouse_ip = get_user_input("Inserisci l'IP del lighthouse")
    real_ip = get_user_input("Inserisci l'IP Reale del lighthouse")
    lighthouse_security_domains = get_user_input("Inserisci i domini per il lighthouse (separati da virgola)")
    generate_certificates(org_name, lighthouse_name, lighthouse_ip, lighthouse_security_domains)
    generate_config(org_name, lighthouse_name, lighthouse_ip, real_ip, lighthouse_security_domains.split(','), is_lighthouse=True)

    client1_name = get_user_input("Inserisci il nome del client 1")
    client1_ip = get_user_input("Inserisci l'IP del client 1")
    client1_security_domains = get_user_input("Inserisci i domini  per il client 1 (separati da virgola)")
    generate_certificates(org_name, client1_name, client1_ip, client1_security_domains)
    generate_config(org_name, client1_name, lighthouse_ip, real_ip, client1_security_domains.split(','))

    client2_name = get_user_input("Inserisci il nome del client 2")
    client2_ip = get_user_input("Inserisci l'IP del client 2")
    client2_security_domains = get_user_input("Inserisci i domini per il client 2 (separati da virgola)")
    generate_certificates(org_name, client2_name, client2_ip, client2_security_domains)
    generate_config(org_name, client2_name, lighthouse_ip, real_ip, client2_security_domains.split(','))

    resources = [
        {"name": lighthouse_name, "security_domains": lighthouse_security_domains},
        {"name": client1_name, "security_domains": client1_security_domains},
        {"name": client2_name, "security_domains": client2_security_domains},
    ]

    check_security_domain_overlap(resources)
