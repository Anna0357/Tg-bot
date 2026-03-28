import json
from collections import defaultdict
from pathlib import Path

_DATA = Path(__file__).resolve().parent.parent / "data"


def load_quiz() -> list[dict]:
    path = _DATA / "quiz_questions.json"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return list(data["questions"])


def load_professions() -> dict[str, dict]:
    path = _DATA / "professions.json"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return {d["id"]: d for d in data["directions"]}


def load_hobbies_by_direction() -> dict[str, dict]:
    path = _DATA / "hobbies_by_direction.json"
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    return dict(data.get("by_direction") or {})


def merge_scores(total: dict[str, int], delta: dict[str, int]) -> None:
    for key, value in delta.items():
        total[key] = total.get(key, 0) + int(value)


def ordered_direction_ids(accumulated: dict[str, int], top_n: int = 3) -> list[str]:
    if not accumulated:
        return []
    ordered = sorted(accumulated.items(), key=lambda x: x[1], reverse=True)
    top_ids = [d_id for d_id, score in ordered[:top_n] if score > 0]
    if not top_ids:
        top_ids = [d_id for d_id, _ in ordered[:top_n]]
    return top_ids


def primary_direction_id(accumulated: dict[str, int]) -> str | None:
    ids = ordered_direction_ids(accumulated, top_n=1)
    return ids[0] if ids else None


def build_directions_message(
    accumulated: dict[str, int],
    professions_by_id: dict[str, dict],
    top_n: int = 3,
) -> str:
    if not accumulated:
        return "Пока мало данных для рекомендации — попробуй пройти тест ещё раз."

    top_ids = ordered_direction_ids(accumulated, top_n=top_n)
    lines = [
        "<b>Твоё направление по ответам теста</b>",
        "(это не диагноз, а повод узнать больше о себе и профессиях):",
        "",
    ]
    for d_id in top_ids:
        info = professions_by_id.get(d_id)
        if not info:
            continue
        lines.append(f"• <b>{info['title']}</b>")
        lines.append(f"  {info['description']}")
        lines.append("")

    lines.append(
        "Обсуди результат с учителем, родителями или профориентологом — "
        "они помогут сузить выбор."
    )
    return "\n".join(lines).strip()


def build_hobbies_message(
    direction_id: str | None,
    professions_by_id: dict[str, dict],
    hobbies_by_direction: dict[str, dict],
) -> str:
    lines = [
        "<b>Кружки и хобби в духе твоего направления</b>",
        "Так можно развить интересы до того, как выбирать вуз или колледж:",
        "",
    ]

    block = direction_id and hobbies_by_direction.get(direction_id)
    if block and direction_id:
        title = professions_by_id.get(direction_id, {}).get("title", direction_id)
        lines.append(f"Опираемся на ближайшее направление: <b>{title}</b>")
        lines.append("")

        clubs = block.get("clubs_examples") or []
        if clubs:
            lines.append("<b>Идеи кружков и внеурочек</b>")
            for item in clubs:
                lines.append(f"• {item}")
            lines.append("")

        hobbies = block.get("hobbies_examples") or []
        if hobbies:
            lines.append("<b>Идеи хобби дома и в свободное время</b>")
            for item in hobbies:
                lines.append(f"• {item}")
            lines.append("")
    else:
        lines.append(
            "Подходящий блок под твой результат пока не найден — "
            "загляни в раздел «О профессиях» и спроси у педагога про кружки в школе и районе."
        )
        lines.append("")

    lines.append(
        "Ищи кружки в школе, доме детского творчества и на портале дополнительного образования твоего региона."
    )
    return "\n".join(lines).strip()


def empty_scores() -> defaultdict[str, int]:
    return defaultdict(int)
