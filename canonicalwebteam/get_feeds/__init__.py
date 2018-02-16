import feedparser
import logging
import json
import time
from datetime import datetime
from requests_cache import CachedSession
from django.conf import settings
from prometheus_client import Counter, Histogram
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


# Settings
requests_timeout = getattr(settings, 'FEED_TIMEOUT', 10)
expiry_seconds = getattr(settings, 'FEED_EXPIRY', 300)
logger = logging.getLogger(__name__)

# Prometheus metric exporters
requested_from_cache_counter = Counter(
    'feed_requested_from_cache',
    'A counter of requests retrieved from the cache',
    ['domain'],
)
failed_requests = Counter(
    'feed_failed_requests',
    'A counter of requests retrieved from the cache',
    ['error_name', 'domain'],
)
request_latency_seconds = Histogram(
    'feed_request_latency_seconds',
    'Feed requests retrieved',
    ['domain', 'code'],
    buckets=[0.25, 0.5, 0.75, 1, requests_timeout],
)

cached_request = CachedSession(
    expire_after=expiry_seconds,
)


def _get(url):
    try:
        response = cached_request.get(url, timeout=requests_timeout)

        if response.from_cache:
            requested_from_cache_counter.labels(
                domain=urlparse(url).netloc,
            ).inc()
        else:
            request_latency_seconds.labels(
                domain=urlparse(url).netloc,
                code=response.status_code,
            ).observe(response.elapsed.total_seconds())

        response.raise_for_status()
    except Exception as request_error:
        failed_requests.labels(
            error_name=type(request_error).__name__,
            domain=urlparse(url).netloc,
        ).inc()
        logger.warning(
            'Attempt to get feed failed: {}'.format(str(request_error))
        )
        return False

    return response


def get_json_feed_content(url, offset=0, limit=None):
    """
    Get the entries in a JSON feed
    """

    end = limit + offset if limit is not None else None

    response = _get(url)

    try:
        content = json.loads(response.text)
    except Exception as parse_error:
        logger.warning(
            'Failed to parse feed from {}: {}'.format(url, str(parse_error))
        )
        return False

    return content[offset:end]


def get_rss_feed_content(url, offset=0, limit=None, exclude_items_in=None):
    """
    Get the entries from an RSS feed
    """

    end = limit + offset if limit is not None else None

    response = _get(url)

    try:
        feed_data = feedparser.parse(response.text)
        if not feed_data.feed:
            logger.warning('No valid feed data found at {}'.format(url))
            return False
        content = feed_data.entries
    except Exception as parse_error:
        logger.warning(
            'Failed to parse feed from {}: {}'.format(url, str(parse_error))
        )
        return False

    if exclude_items_in:
        exclude_ids = [item['guid'] for item in exclude_items_in]
        content = [item for item in content if item['guid'] not in exclude_ids]

    content = content[offset:end]

    for item in content:
        updated_time = time.mktime(item['updated_parsed'])
        item['updated_datetime'] = datetime.fromtimestamp(updated_time)

    return content
