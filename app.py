from copy import deepcopy

from flask import Flask, abort, render_template, request

from data.profile import profile, projects


app = Flask(__name__)

TRANSLATIONS = {
    "en": {
        "lang": "en",
        "html_lang": "en",
        "nav_home": "Home",
        "nav_projects": "Projects",
        "nav_cv": "Resume",
        "hero_badge": "Python portfolio + integrated resume",
        "hero_projects": "View projects",
        "hero_cv": "Open resume",
        "summary_eyebrow": "Professional Summary",
        "summary_title": "Positioned for remote AI training and code evaluation work",
        "work_eyebrow": "Work Style",
        "work_title": "Availability and remote fit",
        "projects_eyebrow": "Projects",
        "projects_title": "Projects selected to match the role requirements",
        "skills_eyebrow": "Skills",
        "skills_title": "Technical keywords aligned to the role",
        "cv_eyebrow": "CV",
        "cv_title": "Resume overview",
        "experience": "Experience",
        "education": "Education",
        "languages": "Languages",
        "view_project": "View project",
        "project_details": "Project Details",
        "back_portfolio": "Back to portfolio",
        "github_profile": "GitHub profile",
        "overview": "Overview",
        "why_matters": "Why this project matters",
        "challenge": "Challenge",
        "solution": "Solution",
        "highlights": "Highlights",
        "key_points": "Key technical points",
        "deliverables": "Deliverables",
        "what_demo": "What this project demonstrates",
        "live_demo": "Live Demo",
        "role": "Role",
        "focus": "Focus",
        "mode": "Mode",
        "stack": "Stack",
        "python_analysis": "Python + analysis",
        "quality_reasoning": "Quality and reasoning",
        "remote_ready": "Remote-ready",
        "filter_all": "All",
        "lang_pt": "Português",
        "lang_en": "English",
    },
    "pt": {
        "lang": "pt",
        "html_lang": "pt-BR",
        "nav_home": "Inicio",
        "nav_projects": "Projetos",
        "nav_cv": "Curriculo",
        "hero_badge": "Portfolio em Python + curriculo integrado",
        "hero_projects": "Ver projetos",
        "hero_cv": "Abrir curriculo",
        "summary_eyebrow": "Resumo Profissional",
        "summary_title": "Posicionado para trabalho remoto com IA e avaliacao de codigo",
        "work_eyebrow": "Estilo de Trabalho",
        "work_title": "Disponibilidade e perfil remoto",
        "projects_eyebrow": "Projetos",
        "projects_title": "Projetos selecionados para combinar com a vaga",
        "skills_eyebrow": "Habilidades",
        "skills_title": "Palavras-chave tecnicas alinhadas a vaga",
        "cv_eyebrow": "CV",
        "cv_title": "Visao geral do curriculo",
        "experience": "Experiencia",
        "education": "Formacao",
        "languages": "Idiomas",
        "view_project": "Ver projeto",
        "project_details": "Detalhes do Projeto",
        "back_portfolio": "Voltar ao portfolio",
        "github_profile": "Perfil no GitHub",
        "overview": "Visao Geral",
        "why_matters": "Por que este projeto importa",
        "challenge": "Desafio",
        "solution": "Solucao",
        "highlights": "Destaques",
        "key_points": "Pontos tecnicos principais",
        "deliverables": "Entregas",
        "what_demo": "O que este projeto demonstra",
        "live_demo": "Demo",
        "role": "Papel",
        "focus": "Foco",
        "mode": "Modo",
        "stack": "Stack",
        "python_analysis": "Python + analise",
        "quality_reasoning": "Qualidade e raciocinio",
        "remote_ready": "Pronto para remoto",
        "filter_all": "Todos",
        "lang_pt": "Português",
        "lang_en": "English",
    },
}


PT_PROFILE = {
    "role": "Engenheiro de Software Python | Revisao de Codigo com IA | Remoto",
    "target_role": "Cargo-alvo: Python Software Engineer - Remote",
    "hero_intro": (
        "Engenheiro Python com foco em codigo limpo, resolucao analitica de problemas, "
        "qualidade de software e entregas confiaveis para times remotos."
    ),
    "summary": (
        "Profissional de software com experiencia pratica em Python, forte atencao aos detalhes "
        "e foco crescente em avaliar qualidade de codigo, identificar bugs e produzir feedback tecnico claro. "
        "Este portfolio foi estruturado para trabalho remoto, projetos de avaliacao de codigo com IA, "
        "criacao de desafios tecnicos e analise estruturada."
    ),
    "strengths": [
        "Revisao de codigo com foco em corretude, clareza e boas praticas",
        "Feedback escrito com raciocinio tecnico estruturado",
        "Colaboracao assincrona e organizacao para trabalho remoto",
        "Experiencia pratica com Python, debugging e automacao",
    ],
    "availability": [
        "Totalmente remoto",
        "Agenda flexivel",
        "Disponivel para projetos assincronos",
        "Baseado na America Latina",
    ],
    "project_categories": ["Todos", "Python", ".NET", "QA / Analysis"],
    "skills": [
        "Python",
        "Flask",
        "Revisao de Codigo",
        "Debugging",
        "Resolucao de Problemas",
        "Redacao Tecnica",
        "Avaliacao de Respostas de IA",
        "Criacao de Desafios Tecnicos",
        "JavaScript",
        "TypeScript",
        "Git",
        "HTML/CSS",
    ],
    "experience": [
        {
            "title": "Desenvolvedor Python",
            "company": "Projetos Independentes",
            "period": "2023 - Atual",
            "items": [
                "Desenvolvimento de aplicacoes em Python focadas em clareza de fluxo, automacao e resolucao pratica de problemas.",
                "Revisao de implementacoes, rastreamento de bugs e melhoria de qualidade por meio de testes e refinamentos iterativos.",
                "Documentacao de decisoes tecnicas para apoiar manutencao e colaboracao assincrona.",
            ],
        },
        {
            "title": "Estudante de Sistemas e Solucoes",
            "company": "Desenvolvimento Academico e Pratico",
            "period": "2022 - Atual",
            "items": [
                "Construcao de base tecnica em engenharia de software, analise de sistemas e estrutura de aplicacoes.",
                "Aplicacao de conceitos academicos em projetos praticos com enfase em logica, qualidade e consistencia.",
                "Fortalecimento do raciocinio analitico por meio de exercicios praticos, debugging e iteracao de projetos.",
            ],
        },
    ],
    "education": [
        {
            "course": "Analise e Desenvolvimento de Sistemas",
            "institution": "Ultimo semestre",
            "period": "Atual",
        }
    ],
    "languages": ["Portugues - Nativo", "Ingles - Intermediario"],
}


PT_PROJECTS = {
    "ai-code-review-sandbox": {
        "tagline": "Fluxo estruturado para analise de codigo gerado por IA.",
        "description": "Ambiente estruturado para inspecionar codigo gerado, comparar saidas, identificar falhas logicas e documentar qualidade com criterios consistentes.",
        "impact": "Demonstra revisao de corretude, deteccao de bugs e disciplina de feedback.",
        "challenge": "Trabalhos de treinamento de IA dependem de revisao de codigo com consistencia, clareza e metodo repetivel.",
        "solution": "Este projeto simula uma interface leve de revisao onde o codigo gerado pode ser analisado por corretude, qualidade e aderencia as instrucoes.",
        "highlights": [
            "Checklist de revisao para corretude, estilo e edge cases",
            "Modelo estruturado de pontuacao de qualidade",
            "Blocos de feedback tecnico com justificativa clara",
            "Navegacao pensada para trabalho assincrono",
        ],
        "deliverables": [
            "Criterios reutilizaveis de revisao",
            "Estrutura de triagem de bugs",
            "Apresentacao orientada a feedback",
            "Demonstracao alinhada a avaliacao de IA",
        ],
    },
    "python-challenge-generator": {
        "tagline": "Criacao de desafios e prompts tecnicos para avaliacao.",
        "description": "Projeto voltado a criacao de desafios de codigo, edge cases e tarefas de avaliacao para medir raciocinio, qualidade de implementacao e aderencia a instrucoes.",
        "impact": "Reforca alinhamento com treinamento de IA, escrita de desafios e pensamento analitico.",
        "challenge": "Programas de avaliacao de IA precisam de perguntas tecnicas bem definidas que testem qualidade de implementacao e nao apenas sintaxe.",
        "solution": "Este projeto apresenta uma estrutura para criar desafios Python com niveis de dificuldade, saidas esperadas, restricoes e notas de avaliacao.",
        "highlights": [
            "Fluxo de criacao baseado em nivel e tema",
            "Mapeamento de edge cases para avaliacao mais forte",
            "Prompts alinhados a verificacao de instrucoes",
            "Separacao clara entre pergunta, restricoes e raciocinio esperado",
        ],
        "deliverables": [
            "Padroes de enunciado",
            "Documentacao de edge cases",
            "Escrita de desafios com foco em avaliacao",
            "Prova de design analitico no portfolio",
        ],
    },
    "remote-productivity-portal": {
        "tagline": "Organizacao remote-first para colaboracao assincrona.",
        "description": "Portal interno para organizar tarefas, referencias e atualizacoes assincronas de equipes distribuidas com agendas flexiveis.",
        "impact": "Reforca prontidao para colaboracao independente e remota.",
        "challenge": "Times distribuidos perdem tempo quando referencias, atualizacoes e prioridades ficam espalhadas em varias ferramentas.",
        "solution": "Este projeto centraliza referencias de trabalho, contexto de progresso e visibilidade de tarefas em uma interface simples.",
        "highlights": [
            "Atualizacoes assincronas organizadas",
            "Referencias centralizadas",
            "Interface simples para rotina remota",
            "Foco pratico em autonomia e clareza",
        ],
        "deliverables": [
            "Modelo de visibilidade de tarefas",
            "Estrutura de fluxo remoto",
            "Layout claro de comunicacao",
            "Evidencia de pensamento para times remotos",
        ],
    },
    "bug-triage-board": {
        "tagline": "Fluxo de priorizacao para debugging e classificacao de issues.",
        "description": "Projeto focado em identificar, categorizar e priorizar problemas de software usando impacto, severidade e clareza de reproducao.",
        "impact": "Mostra debugging estruturado, priorizacao e criterio de engenharia.",
        "challenge": "Equipes perdem tempo quando bugs sao reportados sem prioridade consistente ou contexto suficiente para agir.",
        "solution": "Este projeto apresenta um fluxo compacto de triagem onde bugs podem ser ordenados por severidade, reproducao e impacto.",
        "highlights": [
            "Classificacao por severidade",
            "Contexto claro de reproducao",
            "Foco na qualidade do fluxo de debugging",
            "Priorizacao pensada para times assincronos",
        ],
        "deliverables": [
            "Categorias de triagem",
            "Pontuacao de prioridade",
            "Revisao de issues com foco em engenharia",
            "Evidencia de maturidade em debugging",
        ],
    },
    "api-response-auditor": {
        "tagline": "Verificacoes de consistencia para respostas estruturadas de API.",
        "description": "Projeto que inspeciona respostas simuladas de API para verificar estrutura, campos ausentes, consistencia de status e confiabilidade da saida.",
        "impact": "Destaca pensamento backend, disciplina de validacao e analise de respostas.",
        "challenge": "Muitos erros de aplicacao surgem de respostas incompletas ou inconsistentes que nao sao validadas cedo.",
        "solution": "Este projeto simula uma ferramenta de auditoria para checar payloads contra regras esperadas e expor falhas antes do impacto no sistema.",
        "highlights": [
            "Verificacao orientada a schema",
            "Saida de auditoria legivel",
            "Atencao a consistencia backend",
            "Mentalidade pratica de validacao de dados",
        ],
        "deliverables": [
            "Analise de payloads",
            "Validacao de regras de resposta",
            "Fluxo de visibilidade de erros",
            "Prova de revisao de qualidade de API",
        ],
    },
    "test-case-studio": {
        "tagline": "Design de testes para edge cases, corretude e confiabilidade.",
        "description": "Projeto centrado em criar cenarios de teste, identificar edge cases e organizar ideias de cobertura para avaliacao confiavel de codigo.",
        "impact": "Demonstra pensamento analitico, estrategia de validacao e foco em qualidade.",
        "challenge": "Codigo pode parecer correto em exemplos simples, mas falhar em edge cases ou entradas inesperadas.",
        "solution": "Este projeto organiza planejamento de testes em torno de fluxo normal, limites, entradas invalidas e saidas esperadas.",
        "highlights": [
            "Pensamento orientado a edge cases",
            "Categorias de cobertura",
            "Estrategia de validacao de corretude",
            "Forte alinhamento com avaliacao de codigo e IA",
        ],
        "deliverables": [
            "Planejamento de cenarios",
            "Estrutura de cobertura",
            "Mentalidade de garantia de qualidade",
            "Evidencia de validacao rigorosa",
        ],
    },
    "dotnet-api-monitor": {
        "tagline": "Monitoramento de saude e resposta para APIs em ASP.NET Core.",
        "description": "Projeto orientado a .NET para inspecionar endpoints de API, tempos de resposta, comportamento de status e sinais de saude operacional.",
        "impact": "Amplia o portfolio com observabilidade backend e raciocinio em ASP.NET Core.",
        "challenge": "Servicos backend precisam de visibilidade rapida sobre falhas, latencia e endpoints instaveis.",
        "solution": "Este projeto simula um dashboard leve de monitoramento com resumos de status, indicadores de latencia e diagnosticos acionaveis.",
        "highlights": [
            "Alinhamento com ASP.NET Core",
            "Mentalidade de observabilidade backend",
            "Acompanhamento de saude de endpoints",
            "Suporte a debugging operacional",
        ],
        "deliverables": [
            "Visao de status de API",
            "Modelo de inspecao de latencia",
            "Perspectiva de confiabilidade backend",
            "Evidencia de pensamento backend em .NET",
        ],
    },
    "dotnet-validation-lab": {
        "tagline": "Validacao de entrada e tratamento estruturado de erros em C#.",
        "description": "Projeto criado para demonstrar regras de validacao, mensagens de erro consistentes e tratamento mais seguro de requisicoes em aplicacoes .NET.",
        "impact": "Mostra disciplina pratica de engenharia em C# com foco em validacao e confiabilidade.",
        "challenge": "Entradas sem validacao geram comportamento instavel, erros inconsistentes e debugging mais dificil.",
        "solution": "Este projeto modela um fluxo orientado a validacao para processar requisicoes com retorno claro de erros e verificacoes de regras.",
        "highlights": [
            "Design backend orientado a validacao",
            "Mensagens de erro legiveis",
            "Foco forte em confiabilidade",
            "Sinal claro de engenharia .NET",
        ],
        "deliverables": [
            "Verificacao de regras de validacao",
            "Mensagens de erro estruturadas",
            "Revisao da qualidade de requisicoes",
            "Prova de resolucao de problemas em .NET",
        ],
    },
}


def localize_profile(lang):
    localized = deepcopy(profile)
    if lang != "pt":
        return localized

    for key, value in PT_PROFILE.items():
        localized[key] = deepcopy(value)

    localized_projects = []
    for project in projects:
        item = deepcopy(project)
        overrides = PT_PROJECTS.get(project["slug"], {})
        item.update(deepcopy(overrides))
        localized_projects.append(item)
    localized["projects"] = localized_projects
    return localized


def get_lang():
    lang = request.args.get("lang", "en").lower()
    return lang if lang in TRANSLATIONS else "en"


REVIEW_SAMPLES = {
    "factorial": {
        "label": "Factorial Function",
        "prompt": "Create a Python function that returns the factorial of a non-negative integer.",
        "code": """def factorial(n):
    result = 0
    for i in range(1, n):
        result *= i
    return result""",
        "issues": [
            {
                "title": "Incorrect initialization",
                "detail": "The accumulator starts at 0, so every multiplication keeps the result at 0.",
                "category": "correctness",
            },
            {
                "title": "Loop excludes the final multiplier",
                "detail": "The range stops before n, so the logic misses the last required multiplication.",
                "category": "instruction_following",
            },
            {
                "title": "No edge-case handling",
                "detail": "The function does not guard negative values or explicitly validate the input.",
                "category": "quality",
            },
        ],
        "positive_notes": [
            "The function name is clear and readable.",
            "The implementation is compact and easy to inspect.",
        ],
    },
    "emails": {
        "label": "Email Validator",
        "prompt": "Write a Python function to validate that an email contains '@' and a domain suffix.",
        "code": """def is_valid_email(value):
    if "@" not in value:
        return False
    local, domain = value.split("@")
    return "." in local""",
        "issues": [
            {
                "title": "Checks dot in the wrong segment",
                "detail": "The validation looks for '.' in the local part instead of the domain.",
                "category": "correctness",
            },
            {
                "title": "Unsafe split behavior",
                "detail": "Using split without constraining the result can break when the string contains more than one '@'.",
                "category": "quality",
            },
        ],
        "positive_notes": [
            "The first guard clause catches a common invalid input quickly.",
            "The function returns booleans consistently.",
        ],
    },
}

CHALLENGE_LIBRARY = {
    "arrays": {
        "title": "Sliding Window Alert",
        "brief": "Analyze a list of values and detect the first subarray that exceeds a threshold.",
        "constraints": [
            "Handle empty lists safely",
            "Support repeated values",
            "Return the starting index or -1 if not found",
        ],
        "test_cases": [
            "[3, 1, 4, 1, 5], window=3, threshold=8 -> 0",
            "[1, 1, 1, 1], window=2, threshold=5 -> -1",
        ],
    },
    "strings": {
        "title": "Instruction-Following Formatter",
        "brief": "Normalize a sentence while preserving word order and removing duplicated whitespace.",
        "constraints": [
            "Keep punctuation untouched",
            "Avoid regex-only solutions",
            "Return an empty string if the input is empty",
        ],
        "test_cases": [
            "'hello   world' -> 'hello world'",
            "' keep   punctuation! ' -> 'keep punctuation!'",
        ],
    },
    "apis": {
        "title": "Async Retry Planner",
        "brief": "Design a function that schedules retries for failed API calls using exponential backoff.",
        "constraints": [
            "Cap the retry delay",
            "Reject invalid retry counts",
            "Return a list of retry timestamps or offsets",
        ],
        "test_cases": [
            "retries=3, base=2 -> [2, 4, 8]",
            "retries=0, base=2 -> []",
        ],
    },
}

REMOTE_TASKS = [
    {
        "title": "Review AI-generated Python solution",
        "status": "In Review",
        "priority": "High",
        "owner": "Gabriel",
    },
    {
        "title": "Draft challenge prompt with edge cases",
        "status": "Planned",
        "priority": "Medium",
        "owner": "Gabriel",
    },
    {
        "title": "Organize async notes for weekly handoff",
        "status": "Done",
        "priority": "Low",
        "owner": "Gabriel",
    },
    {
        "title": "Validate scoring rubric against guidelines",
        "status": "In Review",
        "priority": "High",
        "owner": "Gabriel",
    },
]

REMOTE_UPDATES = [
    "Reviewed two generated solutions and documented the main correctness issues.",
    "Prepared a challenge outline with instructions, expected outputs, and edge cases.",
    "Consolidated async notes to make handoff easier for distributed collaboration.",
]

BUG_REPORTS = [
    {
        "title": "Login button freezes on slow network",
        "severity": "High",
        "impact": "Users cannot complete sign-in reliably.",
        "status": "Needs Fix",
    },
    {
        "title": "Profile image fails on first load",
        "severity": "Medium",
        "impact": "Visual regression with fallback missing.",
        "status": "Investigating",
    },
    {
        "title": "Dashboard counter off by one",
        "severity": "Low",
        "impact": "Minor reporting mismatch in summary card.",
        "status": "Backlog",
    },
]

API_PAYLOADS = {
    "orders": {
        "label": "Orders Endpoint",
        "payload": """{
  "status": 200,
  "orders": [
    {"id": 101, "total": 49.9, "currency": "BRL"},
    {"id": 102, "currency": "BRL"}
  ]
}""",
        "issues": [
            "Second order is missing the 'total' field.",
            "No pagination metadata is returned for a collection endpoint.",
        ],
    },
    "user": {
        "label": "User Profile Endpoint",
        "payload": """{
  "status": 200,
  "user": {
    "id": 7,
    "name": "Gabriel",
    "email": null
  }
}""",
        "issues": [
            "Email is null even though the client expects a string.",
            "No explicit updated timestamp is provided for cache validation.",
        ],
    },
}

TEST_SCENARIOS = {
    "sorting": {
        "title": "Sorting Function",
        "cases": [
            "Normal case: [3, 1, 2] -> [1, 2, 3]",
            "Edge case: [] -> []",
            "Boundary case: [1] -> [1]",
            "Duplicate values: [2, 2, 1] -> [1, 2, 2]",
        ],
    },
    "calculator": {
        "title": "Calculator Division",
        "cases": [
            "Normal case: 10 / 2 -> 5",
            "Edge case: 0 / 5 -> 0",
            "Invalid input: 5 / 0 -> handled error",
            "Negative values: -9 / 3 -> -3",
        ],
    },
}

DOTNET_ENDPOINTS = [
    {
        "name": "GET /api/orders",
        "status": "Healthy",
        "latency": "82 ms",
        "note": "Stable response time and valid payload contract.",
    },
    {
        "name": "POST /api/payments",
        "status": "Warning",
        "latency": "241 ms",
        "note": "Latency spike detected during peak load simulation.",
    },
    {
        "name": "GET /api/users/{id}",
        "status": "Critical",
        "latency": "510 ms",
        "note": "Intermittent null payload found in profile response.",
    },
]

DOTNET_VALIDATION_CASES = {
    "registration": {
        "label": "User Registration DTO",
        "request": """{
  "name": "",
  "email": "gabriel.com",
  "age": 15
}""",
        "errors": [
            "Name is required.",
            "Email must be a valid email address.",
            "Age must be at least 18.",
        ],
    },
    "invoice": {
        "label": "Invoice Request DTO",
        "request": """{
  "customerId": 0,
  "amount": -45,
  "currency": ""
}""",
        "errors": [
            "CustomerId must be greater than zero.",
            "Amount must be positive.",
            "Currency is required.",
        ],
    },
}


def build_review_demo(sample_key):
    sample = REVIEW_SAMPLES.get(sample_key, REVIEW_SAMPLES["factorial"])
    issue_count = len(sample["issues"])
    score = max(58, 96 - issue_count * 12)
    return {
        "selected_key": sample_key if sample_key in REVIEW_SAMPLES else "factorial",
        "samples": REVIEW_SAMPLES,
        "sample": sample,
        "score": score,
        "quality_flags": [
            "Correctness" if any(item["category"] == "correctness" for item in sample["issues"]) else "Stable",
            "Instruction Following" if any(item["category"] == "instruction_following" for item in sample["issues"]) else "Aligned",
            "Code Quality" if any(item["category"] == "quality" for item in sample["issues"]) else "Readable",
        ],
    }


def build_challenge_demo(topic, difficulty):
    selected_topic = topic if topic in CHALLENGE_LIBRARY else "arrays"
    selected_difficulty = difficulty if difficulty in {"junior", "mid", "senior"} else "mid"
    challenge = CHALLENGE_LIBRARY[selected_topic]
    difficulty_labels = {
        "junior": "Junior",
        "mid": "Mid-Level",
        "senior": "Senior",
    }
    expectations = {
        "junior": "Focus on correctness, readable control flow, and basic input validation.",
        "mid": "Expect edge-case handling, clarity, and good decomposition choices.",
        "senior": "Expect strong tradeoff reasoning, scalable logic, and explicit assumptions.",
    }
    return {
        "topics": CHALLENGE_LIBRARY,
        "selected_topic": selected_topic,
        "selected_difficulty": selected_difficulty,
        "difficulty_label": difficulty_labels[selected_difficulty],
        "expectation": expectations[selected_difficulty],
        "challenge": challenge,
    }


def build_productivity_demo(status_filter):
    valid_filters = {"all", "Planned", "In Review", "Done"}
    selected_filter = status_filter if status_filter in valid_filters else "all"
    filtered_tasks = [
        task for task in REMOTE_TASKS if selected_filter == "all" or task["status"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "tasks": filtered_tasks,
        "stats": {
            "planned": sum(task["status"] == "Planned" for task in REMOTE_TASKS),
            "in_review": sum(task["status"] == "In Review" for task in REMOTE_TASKS),
            "done": sum(task["status"] == "Done" for task in REMOTE_TASKS),
        },
        "updates": REMOTE_UPDATES,
    }


def build_bug_triage_demo(severity_filter):
    valid_filters = {"all", "High", "Medium", "Low"}
    selected_filter = severity_filter if severity_filter in valid_filters else "all"
    reports = [
        bug for bug in BUG_REPORTS if selected_filter == "all" or bug["severity"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "reports": reports,
        "stats": {
            "high": sum(item["severity"] == "High" for item in BUG_REPORTS),
            "medium": sum(item["severity"] == "Medium" for item in BUG_REPORTS),
            "low": sum(item["severity"] == "Low" for item in BUG_REPORTS),
        },
    }


def build_api_auditor_demo(payload_key):
    selected_key = payload_key if payload_key in API_PAYLOADS else "orders"
    payload = API_PAYLOADS[selected_key]
    return {
        "selected_key": selected_key,
        "payloads": API_PAYLOADS,
        "payload": payload,
        "score": max(70, 95 - len(payload["issues"]) * 8),
    }


def build_test_case_demo(scenario_key):
    selected_key = scenario_key if scenario_key in TEST_SCENARIOS else "sorting"
    return {
        "selected_key": selected_key,
        "scenarios": TEST_SCENARIOS,
        "scenario": TEST_SCENARIOS[selected_key],
    }


def build_dotnet_monitor_demo(status_filter):
    valid_filters = {"all", "Healthy", "Warning", "Critical"}
    selected_filter = status_filter if status_filter in valid_filters else "all"
    endpoints = [
        item for item in DOTNET_ENDPOINTS if selected_filter == "all" or item["status"] == selected_filter
    ]
    return {
        "selected_filter": selected_filter,
        "endpoints": endpoints,
        "stats": {
            "healthy": sum(item["status"] == "Healthy" for item in DOTNET_ENDPOINTS),
            "warning": sum(item["status"] == "Warning" for item in DOTNET_ENDPOINTS),
            "critical": sum(item["status"] == "Critical" for item in DOTNET_ENDPOINTS),
        },
    }


def build_dotnet_validation_demo(case_key):
    selected_key = case_key if case_key in DOTNET_VALIDATION_CASES else "registration"
    return {
        "selected_key": selected_key,
        "cases": DOTNET_VALIDATION_CASES,
        "case": DOTNET_VALIDATION_CASES[selected_key],
        "score": max(72, 96 - len(DOTNET_VALIDATION_CASES[selected_key]["errors"]) * 6),
    }


@app.route("/")
def index():
    lang = get_lang()
    return render_template(
        "index.html",
        profile=localize_profile(lang),
        t=TRANSLATIONS[lang],
        lang=lang,
    )


@app.route("/projects/<slug>")
def project_detail(slug):
    lang = get_lang()
    localized_profile = localize_profile(lang)
    project = next((item for item in localized_profile["projects"] if item["slug"] == slug), None)
    if project is None:
        abort(404)

    demo = None
    if slug == "ai-code-review-sandbox":
        demo = build_review_demo(request.args.get("sample", "factorial"))
    elif slug == "python-challenge-generator":
        demo = build_challenge_demo(
            request.args.get("topic", "arrays"),
            request.args.get("difficulty", "mid"),
        )
    elif slug == "remote-productivity-portal":
        demo = build_productivity_demo(request.args.get("status", "all"))
    elif slug == "bug-triage-board":
        demo = build_bug_triage_demo(request.args.get("severity", "all"))
    elif slug == "api-response-auditor":
        demo = build_api_auditor_demo(request.args.get("payload", "orders"))
    elif slug == "test-case-studio":
        demo = build_test_case_demo(request.args.get("scenario", "sorting"))
    elif slug == "dotnet-api-monitor":
        demo = build_dotnet_monitor_demo(request.args.get("status", "all"))
    elif slug == "dotnet-validation-lab":
        demo = build_dotnet_validation_demo(request.args.get("case", "registration"))

    return render_template(
        "project.html",
        profile=localized_profile,
        project=project,
        demo=demo,
        t=TRANSLATIONS[lang],
        lang=lang,
    )


if __name__ == "__main__":
    app.run(debug=True)
