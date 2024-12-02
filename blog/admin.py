from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment


# Register your models here.
# Post 모델을 등록할 때 MarkdownxModelAdmin을 사용하여 마크다운 렌더링 기능을 활성화
admin.site.register(Post, MarkdownxModelAdmin)

# Category 모델에 대한 관리자 설정
class CategoryAdmin(admin.ModelAdmin):
    # 'name' 필드를 바탕으로 자동으로 'slug' 필드를 생성하도록 설정
    prepopulated_fields = {'slug': ('name', )}

# Category 모델을 관리자에 등록
admin.site.register(Category, CategoryAdmin)

# Tag 모델에 대한 관리자 설정
class TagAdmin(admin.ModelAdmin):
    # 'name' 필드를 바탕으로 자동으로 'slug' 필드를 생성하도록 설정
    prepopulated_fields = {'slug': ('name', )}

# Tag 모델을 관리자에 등록
admin.site.register(Tag, TagAdmin)

# Comment 모델을 관리자에 등록
admin.site.register(Comment)