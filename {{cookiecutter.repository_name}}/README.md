# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Dipendenze

- python
- poetry [pip]
- make (opzionale)
- pytest (opzionale, installata da poetry ma è più comodo averla installata nel sistema) [pip]
- pre-commit (opzionale, installata da poetry ma è più comodo averla installata nel sistema) [pip]
- vagrant e VirtualBox (opzionale)
- pipx (remote machine) [pip]

## Configurazione ambiente di sviluppo

 ```bash
 make init
 ```

- Aprire VSCode e installare le estensioni suggerite

## Packaging

- Aggiornare la versione del progetto con uno dei seguenti comandi (mai aggiornare a mano la versione):

  ```bash
  make bump
  ```

- Pushare i tag per pubblicare il pacchetto nel registry di gitlab

  ```bash
  git push --tags
  ```

## Provision e Deploy

### Dev

```bash
vagrant up      # start the local VM
make provision  # type vagrant
make deploy     # type vagrant
vagrant ssh     # connect to the local VM
```

### Lab/Pro

```bash
make provision
make deploy
```

### Rollback

Se fosse necessario effettuare un rollback di emergenza su un ambiente di produzione, è possibile collegarsi alla macchina ed installare una versione specifica del pacchetto

```bash
pipx install --force {{ cookiecutter.project_slug }}==x.x.x
```

Le versioni disponibili possono essere trovate con il comando (pip >=20.3)

```bash
pip install --use-deprecated=legacy-resolver {{ cookiecutter.project_slug }}==
```
