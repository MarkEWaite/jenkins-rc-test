Jenkins Release Candidate Test Helpers
======================================

Introduction
------------

This set of Jenkins jobs and related scripts assist a skilled Jenkins
user to quickly configure test environments.  The scripts and jobs are
intended to *support and assist* a skilled user or tester in
evaluating a release candidate.  They remove some of the repetitive
portions of environment configuration and perform some sanity checks.
They *do not* replace a skilled user or tester evaluation of recent
changes, recent bug reports, or latest web browser interactions.

Tasks
-----

- Create a bootstrap script which accepts the URL source for the
  Jenkins WAR file as an argument, checks userContent for that WAR
  file, and if it is not found, downloads it to the userContent
  directory

Rationale
---------

Evaluating a Jenkins long term support release candidate needs to
balance many competing priorities.  Some of the competing priorities
include:

- Time constrained - do not unnecessarily delay a release
- Multiple test axes to evaluate, including
    - Operating system
    - Java version
    - Web container (Winstone, Tomcat, WebSphere, etc.)
    - Web browser (IE 7, IE 8, IE 9, IE 10, Chrome, Firefox, Safari, etc.)
    - Locale
- Many plugins to consider - 400+ and growing

The testing is further complicated by the many different ways in which
problems might occur.  In the recent past, we've had cases where a
code improvement (lazy loading of content) caused a serious
performance regression because a plugin exercised worst case behavior
in the improved code.  The general performance without the plugin was
improved, but once the plugin was loaded, performance suffered badly.
