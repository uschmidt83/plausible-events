# plausible-events

This small library allows to use easily use the [Plausible Events API](https://plausible.io/docs/events-api).

- **Privacy-focused.**
  Uses the open-source and [privacy](https://plausible.io/privacy-focused-web-analytics)-focused [Plausible Analytics](https://plausible.io).
  IP addresses are only used to correctly count unique users, but are [never stored](https://plausible.io/privacy-focused-web-analytics#no-personal-data-is-collected) (also not by [ipify](https://www.ipify.org), which is used to obtain the public IP address of the caller).
- **Doesn't slow down the main application.**
  Calls to record events are non-blocking, the necessary http requests happen on a separate thread.
- **Doesn't show errors, but tries again.**
  Failed event recordings are re-tried indefinitely. I.e. no events should be lost if the internet connection is temporarily interrupted.


## Examples

```python
from plausible_events import PlausibleEvents

# create object to record events for your plausible.io domain
pe = PlausibleEvents(domain='my.domain.com')

# record a page view event with a (hypothetical) path
pe.pageview('/login/user')

# record a custom event with additional custom properties
pe.event('my event', dict(os='mac', var='foo'))
```


## What is Plausible Analytics?

[Plausible Analytics](https://plausible.io) is a transparent and fully open source analytics software. From their website:

> Plausible is [open source analytics](https://plausible.io/open-source-website-analytics). Our source code is available and accessible on GitHub so anyone can read it, inspect it and review it to verify that our actions match with our words. We welcome feedback and have a public roadmap. If you're happy to manage your own infrastructure, you can [self-host Plausible](https://plausible.io/self-hosted-web-analytics) too.
