def assess_skill_level(recent_scores, thresholds=(60, 80)):
    """
    Assess skill level based on recent quiz or interaction scores.
    Args:
        recent_scores (list): List of numeric scores (0-100).
        thresholds (tuple): Two threshold values separating levels.
    Returns:
        str: Skill level - 'beginner', 'intermediate', 'advanced'
    """
    if not recent_scores:
        return 'beginner'
    avg_score = sum(recent_scores) / len(recent_scores)
    if avg_score >= thresholds[1]:
        return 'advanced'
    elif avg_score >= thresholds[0]:
        return 'intermediate'
    else:
        return 'beginner'
