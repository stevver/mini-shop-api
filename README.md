# Mini Shop API

Väike Flask REST API, mis demonstreerib DevOps tööriistade koos kasutamist (CI/CD → Docker → Kubernetes → Ansible).

## Kirjeldus
- **Mis see teeb?**
  - Pakub lihtsat “mini-poe” API-d järgmiste endpoint’idega:
    - `GET /` – info + versioon
    - `GET /health` – health check
    - `GET /products` – toodete nimekiri
    - `GET /api/version` – versioon/build info
    - `GET /api/status` – API staatus + endpoint’ide nimekiri
- **Mis probleem lahendab?**
  - Näitab, kuidas automatiseerida arenduse ja paigalduse workflow’d: testid ja build jooksevad automaatselt, Docker image on üheselt versioonitud ning rakendus on deploy’tud Kubernetesesse nii, et sellele saab väljast ligi.

## Tööriistad

### 1. Git
**Miks:** versioonihaldus, ajalugu, lihtne rollback ja arenduse jälgitavus (commit’id).  
Git võimaldab teha muudatusi kontrollitult ja push’ida need CI/CD pipeline’i käivitamiseks.

### 2. GitHub Actions
**Miks:** automaatne CI/CD (koodi kontroll, testid, Docker image build).  
Pipeline aitab leida vigu kiiresti ja tagab, et ainult läbiv kood “läheb edasi”.

### 3. Docker
**Miks:** sama rakendus jookseb igal pool ühtemoodi (lokaalselt, CI-s, Kuberneteses).  
**Kuidas integreerib:** GitHub Actions build’ib Docker image’i ning (vajadusel) push’ib selle registry’sse (nt GHCR). Kubernetes kasutab sama image’i.

### 4. Kubernetes (k3s)
**Miks:** Kubernetes hoiab rakenduse tööle (Deployment, self-healing, skaleerimine).  
**Kuidas integreerib:**
- Kubernetes (k3s) käivitab rakenduse `Deployment`-ina ja teeb selle kättesaadavaks `Service (NodePort)` kaudu.

### 5. Ansible
**Miks:** Ansible automatiseerib deploy/uuenduse.
**Kuidas integreerib:**
- Ansible käivitab `kubectl apply -f k8s/` (või uuendab image tag’i) ja teeb deployment’i korduvkäivitatavaks.

## Käivitamine

### 1) Projekti kloonimine
```bash
git clone https://github.com/stevver/mini-shop-api.git
cd mini-shop-api
```

### 2) Lokaalne käivitamine (Python)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Test:
```bash
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/products
```

### 3) Testid
```bash
pytest -v
```

### 4) Dockeriga
```bash
docker build -t mini-shop-api:local .
docker run --rm -p 5000:5000 mini-shop-api:local
```

Test:
```bash
curl http://127.0.0.1:5000/health
```

### 5) Kubernetes (k3s) deploy
Eeldus: k3s + kubectl olemas.

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

Rakendus (NodePort näide):
- `http://<MASINA_IP>:30080/health`
- `http://<MASINA_IP>:30080/products`

### 6) Deploy Ansible’iga (kui playbook olemas)
```bash
ansible-playbook -i inventory deploy.yml
```

## Kuidas Tööriistad Töötavad Koos

1. Arendaja teeb muudatused ja commit’ib Git’i.
2. `git push` käivitab GitHub Actions pipeline’i (validate → test → build → (push image)).
3. Kubernetes (k3s) jooksutab Docker image’i Deployment’ina; Ansible automatiseerib deploy/uuenduse (kubectl apply / image update).

## Autorid
Stever
