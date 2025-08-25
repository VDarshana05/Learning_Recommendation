def generate_explanations(student_profile, recommended_resources):
    """
    Create human-readable explanations for each recommended resource.
    """
    explanations = []
    skill_map = {'beginner': 'Basic', 'intermediate': 'Intermediate', 'advanced': 'Advanced'}

    for _, resource in recommended_resources.iterrows():
        reasons = []
        if resource['topic'] in student_profile['interests']:
            reasons.append(f"matches your interest in {resource['topic']}")
        reasons.append(f"suitable for {skill_map.get(student_profile['skill_level'], 'Basic')} level")
        reasons.append(f"type: {resource['resource_type']}")
        explanation = "Recommended because it " + ", ".join(reasons) + "."
        explanations.append(explanation)

    return explanations
