from .models import Comment
from django import forms


# CommentForm 클래스: 댓글을 작성하는 폼을 정의하는 클래스
class CommentForm(forms.ModelForm):
    # 메타 클래스에서 사용할 모델과 필드를 정의
    class Meta:
        model = Comment  # 폼이 연결될 모델을 Comment로 지정
        fields = ('content',)  # 댓글의 'content' 필드만 사용 (댓글 내용만 입력받음)