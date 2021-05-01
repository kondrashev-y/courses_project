from django.template import Library
from django.utils.html import mark_safe


register = Library()


@register.filter()
def comments_filter(comments_list):
    res = """
    <ul style="list-style-type:none;">
        <div class="col-md-12 mt-2">
            {}
        </div>
    </ul>
    """
    i = ''
    for comment in comments_list:
        i += """
        <li>
            <div class="col-md-12 mb-2 mt-2 p-o">
                <big>{author}</big> | <small>date: {timestamp}</small>
                <hr>
                <p>{text} | id={id}`</p>
                <a href="#{id}" class="reply" data-id="{id}" data-parent={parent_id}>Ответить</a>
                <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
                    <textarea type="text" class="form-control" name="comment-text"></textarea><br>
                        <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="Отправить">
                </form>
            </div>
        </li>
        """.format(id=comment['id'], author=comment['author'], timestamp=comment['timestamp'], parent_id=comment['parent_id'], text=comment['text'])
        if comment.get('children'):
            i += comments_filter(comment['children'])
    return mark_safe(res.format(i))
