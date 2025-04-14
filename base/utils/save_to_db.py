""" This module contains functions to save items retrieved from the api using the async_task_queue to the database """
from datetime import datetime
from logging import getLogger
from django.utils.timezone import get_current_timezone
from django.db import transaction


from story.models import Story, Comment
from job.models import Job
from user_account.models import User
from poll.models import Poll, PollOption

logger = getLogger(__name__)


async def save_item(*, item: dict):
    try:
        if time := item.get('time'):
            item['time'] = datetime.fromtimestamp(time, get_current_timezone())

        with transaction.atomic():
            if item['type'] == 'story':
                await save_story(story=item)

            elif item['type'] == 'comment':
                await save_comment(comment=item)

            elif item['type'] == 'job':
                await save_job(job=item)

            elif item['type'] == 'poll':
                await save_poll(poll=item)

            elif item['type'] == 'pollopt':
                await save_poll_option(poll_option=item)
    except Exception as err:
        logger.error("%s: Error in creating an item", err)


async def save_comment(*, comment: dict):
    try:
        comment_fields = ['by', 'id', 'parent', 'text', 'time', 'type']
        comment = {field: comment[field] for field in comment_fields if field in comment}
        parent_id = comment.pop('parent')
        parent, parent_type = await get_parent(parent_id=parent_id)
        comment["by"] = await save_user(user={"id": comment.pop("by")})
        comment["item_id"] = item_id = comment.pop("id")
        comment, _ = await Comment.objects.aupdate_or_create(defaults={**comment}, item_id=item_id)
        if parent_type == "story":
            comment.story = parent
            await comment.asave(update_fields=('story',))
        elif parent_type == "comment":
            await parent.replies.aadd(comment)
    except Exception as err:
        logger.error("%s: Error in creating a comment", err)


async def get_parent(*, parent_id):
    try:
        parent = await Story.objects.filter(item_id=parent_id).afirst()
        if parent:
            return parent, 'story'
        comment = await Comment.objects.filter(item_id=parent_id).afirst()
        if comment:
            return comment, 'comment'
        return None, 'dangling'
    except Exception as err:
        logger.error("%s: Error in getting parent", err)


async def save_job(*, job: dict):
    try:
        job_fields = ['by', 'id', 'descendants', 'score', 'time', 'title', 'type', 'text', 'url']
        job = {field: job[field] for field in job_fields if field in job}
        job["by"] = await save_user(user={'id': job.pop('by')})
        await Job.objects.aupdate_or_create(item_id=job.pop("id"), defaults={**job})
    except Exception as err:
        logger.error(f"{err} in creating a job")


async def save_story(*, story: dict):
    try:
        story_fields = ['by', 'id', 'descendants', 'score', 'time', 'title', 'type', 'text', 'url']
        story = {field: story[field] for field in story_fields if field in story}
        story['by'] = await save_user(user={'id': story.pop('by')})
        await Story.objects.aupdate_or_create(item_id=story.pop("id"), defaults={**story})
    except Exception as err:
        logger.error("%s: Error in creating a story", err)


async def save_poll(*, poll: dict):
    try:
        poll_fields = ['by', 'id', 'descendants', 'score', 'time', 'title', 'type', 'text']
        poll = {field: poll[field] for field in poll_fields if field in poll}
        poll['by'] = await save_user(user={'id': poll.pop('by')})
        await Poll.objects.aupdate_or_create(item_id=poll.pop("id"), defaults={**poll})
    except Exception as err:
        logger.error("%s: Error in creating a poll", err)


async def save_poll_option(*, poll_option: dict):
    try:
        poll_opt_fields = ['by', 'id', 'poll', 'text', 'score', 'time', 'type']
        poll_option = {field: poll_option[field] for field in poll_opt_fields if field in poll_option}
        poll = await Poll.objects.filter(item_id=poll_option.pop('poll')).afirst()
        poll_option['poll'] = poll
        poll_option['by'] = await save_user(user={'id': poll_option.pop('by')})
        await PollOption.objects.aupdate_or_create(item_id=poll_option.pop("id"), defaults={**poll_option})
    except Exception as err:
        logger.error("%s: Error in creating a poll option", err)

async def save_user(*, user: dict):
    try:
        with transaction.atomic():
            user_fields = ['id', 'karma', 'about', 'created']
            user = {field: user[field] for field in user_fields if field in user}
            user['username'] = username = user.pop('id')
            user['email'] = f"{username}@zenhn.com"
            if user.get("created"):
                user["created"] = datetime.fromtimestamp(user["created"], tz=get_current_timezone())
            user, created = await User.objects.aupdate_or_create(defaults={**user}, username=username, email=user['email'])
            if created:
                user.set_unusable_password()
                await user.asave(update_fields=('password',))
            return user
    except Exception as err:
        logger.error("%s: Error in creating a user", err)
