from types import SimpleNamespace


def _ns(d: dict) -> SimpleNamespace:
    return SimpleNamespace(**d)


_PT = {
    "html_lang": "pt-BR",
    "nav_home": "Início",
    "nav_projects": "Projetos",
    "nav_cv": "CV",
    # hero
    "hero_badge": "Portfólio & CV",
    "hero_projects": "Ver projetos",
    "hero_cv": "Ver CV",
    # summary
    "summary_eyebrow": "Sobre mim",
    "summary_title": "Resumo profissional",
    # work
    "work_eyebrow": "Disponibilidade",
    "work_title": "Pronto para trabalho remoto",
    # projects
    "projects_eyebrow": "Portfólio",
    "projects_title": "Projetos em destaque",
    "view_project": "Ver projeto",
    # skills
    "skills_eyebrow": "Competências",
    "skills_title": "Stack técnica",
    # cv
    "cv_eyebrow": "Currículo",
    "cv_title": "Experiência & Formação",
    "experience": "Experiência",
    "education": "Formação",
    "languages": "Idiomas",
    # project detail
    "project_details": "Detalhe do projeto",
    "back_portfolio": "← Voltar ao portfólio",
    "github_profile": "GitHub",
    "role": "Cargo",
    "python_analysis": "Engenharia Python",
    "focus": "Foco",
    "quality_reasoning": "Qualidade & Raciocínio",
    "mode": "Modo",
    "remote_ready": "100% Remoto",
    "stack": "Stack",
    "overview": "Visão geral",
    "why_matters": "Por que importa",
    "challenge": "Desafio",
    "solution": "Solução",
    "highlights": "Destaques",
    "key_points": "Pontos-chave",
    "deliverables": "Entregas",
    "what_demo": "O que este projeto demonstra",
    "live_demo": "Demo interativa",
}

_EN = {
    "html_lang": "en",
    "nav_home": "Home",
    "nav_projects": "Projects",
    "nav_cv": "CV",
    # hero
    "hero_badge": "Portfolio & CV",
    "hero_projects": "View projects",
    "hero_cv": "View CV",
    # summary
    "summary_eyebrow": "About me",
    "summary_title": "Professional summary",
    # work
    "work_eyebrow": "Availability",
    "work_title": "Ready for remote work",
    # projects
    "projects_eyebrow": "Portfolio",
    "projects_title": "Featured projects",
    "view_project": "View project",
    # skills
    "skills_eyebrow": "Skills",
    "skills_title": "Technical stack",
    # cv
    "cv_eyebrow": "Resume",
    "cv_title": "Experience & Education",
    "experience": "Experience",
    "education": "Education",
    "languages": "Languages",
    # project detail
    "project_details": "Project detail",
    "back_portfolio": "← Back to portfolio",
    "github_profile": "GitHub",
    "role": "Role",
    "python_analysis": "Python Engineering",
    "focus": "Focus",
    "quality_reasoning": "Quality & Reasoning",
    "mode": "Mode",
    "remote_ready": "100% Remote",
    "stack": "Stack",
    "overview": "Overview",
    "why_matters": "Why it matters",
    "challenge": "Challenge",
    "solution": "Solution",
    "highlights": "Highlights",
    "key_points": "Key points",
    "deliverables": "Deliverables",
    "what_demo": "What this project demonstrates",
    "live_demo": "Live demo",
}

TRANSLATIONS: dict[str, SimpleNamespace] = {
    "pt": _ns(_PT),
    "en": _ns(_EN),
}


def get_t(lang: str) -> SimpleNamespace:
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"])
