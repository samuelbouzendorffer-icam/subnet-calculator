# subnet-calculator

Calculatrice de **sous-réseaux IPv4** en ligne de commande (Python, module `ipaddress` de la bibliothèque standard). Utile pour apprendre l'adressage IP, le masque et le découpage en sous-réseaux.

## Utilisation

```bash
python3 subnet.py info 192.168.1.130/26
```

```
Réseau                192.168.1.128
Préfixe               /26
Masque                255.255.255.192
Masque inverse        0.0.0.63
Broadcast             192.168.1.191
Première machine      192.168.1.129
Dernière machine      192.168.1.190
Machines utilisables  62
Adresse privée        oui
```

```bash
python3 subnet.py split 10.0.0.0/24 --prefix 26      # découpe en 4 sous-réseaux /26
python3 subnet.py contains 192.168.0.0/16 192.168.42.7   # -> oui
python3 subnet.py hosts 50                           # -> /26 (jusqu'à 62 machines)
```

On peut donner une adresse de machine (`192.168.1.130/26`) : l'outil en déduit le réseau auquel elle appartient.

## Concepts illustrés

- **Notation CIDR**, masque de sous-réseau et masque inverse (*wildcard*).
- Adresse réseau, adresse de broadcast et plage d'adresses utilisables (`2^n - 2` machines).
- Cas particuliers : `/31` (liaison point à point, RFC 3021) et `/32` (une seule machine).
- **VLSM** : choisir le plus petit sous-réseau pouvant contenir *N* machines.
- Adresses privées (RFC 1918).

## Tests

```bash
python3 -m unittest -v
```

## Limites

IPv4 uniquement. Le résultat peut être vérifié avec la mémo réseau de mon [journal d'apprentissage](https://github.com/samuelbouzendorffer-icam/cybersec-learning-log).

## Pistes d'amélioration

- Gérer IPv6.
- Proposer un plan d'adressage complet à partir d'une liste de besoins (VLSM sur plusieurs sous-réseaux de tailles différentes).
- Afficher les adresses en binaire pour visualiser le masque.

## Licence

MIT, voir [LICENSE](LICENSE).

---

*Réalisé avec l'aide de Claude (IA), relu et testé par l'auteur.*
