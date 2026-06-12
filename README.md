# 🌱 Grow Your Forest — Simulador de Impacto Ambiental

## 📌 Visão Geral

O **Grow Your Forest** é um MVP (*Minimum Viable Product*) desenvolvido como projeto acadêmico na **CESAR School**.

A solução consiste em uma plataforma de inteligência e análise de dados voltada para a gestão de frotas sustentáveis, permitindo monitorar, mensurar e demonstrar de forma visual e analítica a redução da pegada de carbono (**CO₂**) e os ganhos econômicos obtidos por empresas de logística ao adotarem sistemas de telemetria e passagem automática (Tags) em praças de pedágio.

Ao eliminar paradas desnecessárias em cabines manuais, o sistema contribui para a redução do consumo de combustível, diminuição das emissões atmosféricas e mitigação de impactos ambientais relacionados à operação da frota.

---

## 👥 Integrantes da Equipe

* Anna Clara
* Fabiana Lima
* Felipe Saraiva
* José Bruno
* Lucas Barros
* Renan Vanbasten

---

## 🚀 Tecnologias Utilizadas

A aplicação foi desenvolvida utilizando o ecossistema Python para engenharia e visualização de dados:

* **Python 3.10+** — Linguagem principal da aplicação.
* **Streamlit** — Construção da interface web interativa.
* **PostgreSQL** — Banco de dados relacional para persistência dos dados.
* **SQLAlchemy** — ORM e camada de acesso ao banco de dados.
* **Pandas** — Manipulação e processamento de dados.
* **Plotly Express** e **Plotly Graph Objects** — Construção de dashboards e gráficos interativos.
* **Python-dotenv** — Gerenciamento seguro de variáveis de ambiente.

---

## 🏛️ Arquitetura do Projeto (MVC)

Para garantir organização, manutenibilidade e separação de responsabilidades, o sistema foi estruturado seguindo o padrão arquitetural **MVC (Model-View-Controller)**.

```text
📁 grow-your-forest/
│
├── 📄 app.py                # Ponto de entrada da aplicação
├── 📄 controllers.py        # Controller: navegação e controle de sessão
├── 📄 models.py             # Model: regras de negócio e persistência
├── 📄 views.py              # View: componentes visuais e dashboards
│
├── 📄 .env                  # Variáveis de ambiente (não versionado)
├── 📄 .env.example          # Modelo de configuração
└── 📄 requirements.txt      # Dependências do projeto
```

### 📦 Model (models.py)

Responsável por:

* Conexão com o banco PostgreSQL.
* Persistência dos dados.
* Implementação das regras de negócio.
* Cálculos ambientais baseados nas metodologias do **GHG Protocol** e **IPCC**.
* Processamento das emissões por escopo.

### 🎨 View (views.py)

Responsável por:

* Construção da interface gráfica.
* Formulários de cadastro e consulta.
* Tabelas gerenciais.
* Gráficos interativos utilizando Plotly.
* Visualização de indicadores ESG e ambientais.

### 🎮 Controller (controllers.py)

Responsável por:

* Controle de navegação entre páginas.
* Gerenciamento de sessão dos usuários.
* Controle de autenticação.
* Isolamento de dados por empresa (*Multi-Tenant*).

---

## 🧮 Inteligência de Negócio — Metodologia GHG Protocol

A plataforma calcula o impacto ambiental evitado por meio da utilização de sistemas de passagem automática em pedágios.

### 🚛 Escopo 1 — Emissões Diretas

Calcula o combustível que deixa de ser consumido quando os veículos evitam o processo de:

* Desaceleração
* Marcha lenta em filas
* Arrancadas sucessivas

Essa redução representa uma diminuição direta das emissões provenientes da queima de combustíveis fósseis.

### 🧾 Escopo 3 — Emissões Indiretas

Calcula o impacto ambiental evitado através da eliminação de comprovantes impressos em papel.

Benefícios considerados:

* Redução do consumo de celulose.
* Menor necessidade de produção de papel térmico.
* Redução da exposição ao BPA (*Bisfenol A*).
* Menor geração de resíduos.

---

## 📊 Funcionalidades da Plataforma

A aplicação oferece:

* Cadastro e gerenciamento de empresas.
* Cadastro de veículos e frotas.
* Monitoramento de passagens em pedágios.
* Cálculo automático de emissões evitadas.
* Dashboards ambientais interativos.
* Indicadores ESG.
* Comparativos entre empresas.
* Controle de acesso multiusuário.

---

## 📈 Indicadores Monitorados

Entre os principais indicadores apresentados pela plataforma estão:

* Quantidade de passagens registradas.
* Redução estimada de CO₂.
* Economia de combustível.
* Economia financeira gerada.
* Quantidade de recibos evitados.
* Ranking ambiental entre empresas.
* Evolução temporal dos indicadores ESG.

---

## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/grow-your-forest.git
cd grow-your-forest
```

### 2. Criar Ambiente Virtual

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=seu_host_do_banco
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

---

## 🖥️ Como Executar a Aplicação

Após configurar o ambiente e o banco de dados, execute:

```bash
streamlit run app.py
```

O Streamlit iniciará um servidor local.

Acesse:

```text
http://localhost:8501
```

---

## 🔑 Credenciais de Acesso para Testes

Para validação do comportamento da aplicação e do isolamento de dados entre empresas:

### Empresa A

**Usuário:**

```text
maria@email.com
```

**Senha:**

```text
senha456
```

### Empresa B

Utilize os demais usuários cadastrados na tabela `usuarios` do banco de dados para validar o comportamento multiempresa (*Multi-Tenant*).

---

## 🌎 Impacto Esperado

O Grow Your Forest busca demonstrar como dados e tecnologia podem contribuir para a construção de operações logísticas mais sustentáveis.

Ao transformar informações operacionais em indicadores ambientais mensuráveis, a plataforma permite que empresas acompanhem seus resultados ESG de forma transparente, auxiliando na tomada de decisão e no desenvolvimento de estratégias voltadas à sustentabilidade corporativa.

---

## 🎓 Projeto Acadêmico

Projeto desenvolvido como atividade acadêmica da **CESAR School**, com foco na aplicação prática de conceitos de:

* Engenharia de Software
* Banco de Dados
* Desenvolvimento Web
* Inteligência de Negócios
* Sustentabilidade
* ESG (Environmental, Social and Governance)
* Análise de Dados
