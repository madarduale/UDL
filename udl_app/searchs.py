from itertools import chain
from django.views.generic import ListView
from .models import Course, Quiz, Exam, Message, Discussion, Assignment


class SearchView(ListView):
    template_name = "search.html"
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["count"] = self.count or 0
        context["query"] = self.request.GET.get("q")
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", None)

        if query is not None:
            course_results = Course.objects.search(query)
            quiz_results = Quiz.objects.search(query)
            exam_results = Exam.objects.search(query)
            message_results = Message.objects.search(query)
            discussion_results = Discussion.objects.search(query)
            assignment_results = Assignment.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                course_results, quiz_results, exam_results, message_results,
                discussion_results, assignment_results
            )
            queryset = sorted(
                queryset_chain, key=lambda instance: instance.pk, reverse=True
            )
            self.count = len(queryset)  # since queryset is actually a list
            return queryset
        return Course.objects.none()  # just an empty queryset as default
