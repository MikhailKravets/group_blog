from rest_framework.permissions import BasePermission


# has_permission() - Is... (IsAuthenticated, IsAllowedToArticles)
# has_object_permission() - Has.. (HasArticleUpdatePermission)

class HasArticleUpdate(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):  # if view.action in ('update', 'partial_update', 'delete')
            if obj.user == request.user:
                return True
            return False

        return True
