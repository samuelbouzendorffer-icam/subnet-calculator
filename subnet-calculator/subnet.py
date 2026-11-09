#!/usr/bin/env python3
"""subnet : calculatrice de sous-réseaux IPv4 (module `ipaddress` de la bibliothèque standard).

Commandes : info, split, contains, hosts
"""
import argparse
import ipaddress
import math


def parse_network(cidr: str) -> ipaddress.IPv4Network:
    """Accepte aussi une adresse d'hôte (192.168.1.130/26) et en déduit le réseau."""
    net = ipaddress.ip_network(cidr, strict=False)
    if net.version != 4:
        raise ValueError("Seul IPv4 est géré par cet outil.")
    return net


def usable_hosts(net: ipaddress.IPv4Network) -> int:
    if net.prefixlen == 32:
        return 1
    if net.prefixlen == 31:
        return 2  # liaison point à point (RFC 3021)
    return net.num_addresses - 2  # on retire l'adresse réseau et le broadcast


def describe(cidr: str) -> dict:
    net = parse_network(cidr)
    if net.prefixlen >= 31:
        first, last = net.network_address, net.broadcast_address
    else:
        first, last = net.network_address + 1, net.broadcast_address - 1
    return {
        "network": str(net.network_address),
        "prefix": net.prefixlen,
        "netmask": str(net.netmask),
        "wildcard": str(net.hostmask),
        "broadcast": str(net.broadcast_address),
        "first_host": str(first),
        "last_host": str(last),
        "usable_hosts": usable_hosts(net),
        "private": net.is_private,
    }


def split(cidr: str, new_prefix: int) -> list:
    net = parse_network(cidr)
    if not net.prefixlen < new_prefix <= 32:
        raise ValueError(f"Le nouveau préfixe doit être compris entre /{net.prefixlen + 1} et /32.")
    return [str(s) for s in net.subnets(new_prefix=new_prefix)]


def contains(cidr: str, ip: str) -> bool:
    return ipaddress.ip_address(ip) in parse_network(cidr)


def prefix_for_hosts(hosts: int) -> int:
    """Plus petit sous-réseau (plus grand préfixe) pouvant contenir `hosts` machines."""
    if hosts < 1:
        raise ValueError("Il faut au moins une machine.")
    if hosts == 1:
        return 32
    if hosts == 2:
        return 31
    return 32 - math.ceil(math.log2(hosts + 2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculatrice de sous-réseaux IPv4.")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("info", help="détails d'un réseau"); p.add_argument("cidr")
    p = sub.add_parser("split", help="découpe un réseau en sous-réseaux")
    p.add_argument("cidr"); p.add_argument("--prefix", type=int, required=True)
    p = sub.add_parser("contains", help="une adresse est-elle dans le réseau ?")
    p.add_argument("cidr"); p.add_argument("ip")
    p = sub.add_parser("hosts", help="préfixe minimal pour N machines"); p.add_argument("count", type=int)
    args = parser.parse_args()

    try:
        if args.command == "info":
            labels = {"network": "Réseau", "prefix": "Préfixe", "netmask": "Masque",
                      "wildcard": "Masque inverse", "broadcast": "Broadcast",
                      "first_host": "Première machine", "last_host": "Dernière machine",
                      "usable_hosts": "Machines utilisables", "private": "Adresse privée"}
            for key, value in describe(args.cidr).items():
                shown = f"/{value}" if key == "prefix" else ("oui" if value is True else "non" if value is False else value)
                print(f"{labels[key]:<22}{shown}")
        elif args.command == "split":
            for s in split(args.cidr, args.prefix):
                print(s)
        elif args.command == "contains":
            print("oui" if contains(args.cidr, args.ip) else "non")
        else:
            p = prefix_for_hosts(args.count)
            print(f"/{p} (jusqu'à {usable_hosts(ipaddress.ip_network(f'0.0.0.0/{p}'))} machines)")
    except ValueError as err:
        raise SystemExit(f"Erreur : {err}")


if __name__ == "__main__":
    main()
