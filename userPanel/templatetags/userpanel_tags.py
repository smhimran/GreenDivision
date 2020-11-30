from django import template
from userPanel.models import Submission

register = template.Library()


@register.filter()
def is_solved(problem, profile):
    solved = Submission.objects.filter(
        problem=problem.id).filter(user=profile.id).exists()

    return solved
