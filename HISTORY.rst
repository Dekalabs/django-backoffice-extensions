.. :changelog:

History
-------

4.2.0 (2024-05-03)
++++++++++++++++++

* Feat: improve field displays

4.1.0 (2023-08-01)
++++++++++++++++++

* Feat: added formsets and new styles

4.0.0 (2022-11-15)
++++++++++++++++++

* Feat: migration from bulma to tailwind

3.1.1 (2022-06-17)
++++++++++++++++++

* Fix: Optional default_app_config

3.1.0 (2022-06-17)
++++++++++++++++++

* Feat: Support for Django 4.0

3.0.0 (2022-03-30)
+++++++++++++++++

* Feat: added support to enable multiple backoffice sites in the same project.

2.2.1 (2021-10-22)
+++++++++++++++++

* Feat: statistics_value now with format. 

2.2.0 (2021-10-1)
+++++++++++++++++

* Feat: changed name for actions block in list template
* Feat: added custom converters to export view mixin

2.1.1 (2021-9-27)
+++++++++++++++++

* Feat: added request to filterset class

2.1.0 (2021-9-23)
+++++++++++++++++

* Feat: add get_queryset to (almost) all base views

2.0.2 (2021-5-18)
+++++++++++++++++

* Fix: sidebar groups permissions 

2.0.1 (2021-5-17)
+++++++++++++++++

* Fix: consistent alignment of data in detail view

2.0.0 (2021-4-28)
+++++++++++++++++

* Feat: the navbar has been removed and its content has been added in the sidebar that is fixed to the window.
* Feat: modal has been added to confirm the deletion of an object.
* Feat: templates and style have been changed.
* Feat: selection widgets have been incorporated.
* Feat: bulma's tags are used to display a field of multiple objects.
* Feat: the templates used in the tests have been updated.
* Feat: filters stick to the screen (if problems arise it could be removed).
* Feat: notifications can be removed.

1.2.3 (2021-4-06)
+++++++++++++++++

* Feat: make csv file fields downloadeable
* Fix: repeated results in SearchListMixin
* Fix: typo "uses_template"

1.2.2 (2021-2-24)
+++++++++++++++++

* Fix: links for foreing keys

1.2.1 (2020-12-17)
+++++++++++++++++

* Fix: pagination previous page url
* Fix: empty queryset in exports

1.2.0 (2020-11-18)
+++++++++++++++++

* New styles

1.1.1 (2020-8-19)
+++++++++++++++++

* Fix for loop for active menu
* Delete view handles protection

1.1.0 (2020-8-19)
+++++++++++++++++

* Added delete view
* Show link download for FieldFile
* Footer always at the bottom of the page and menu always have a fixed width
* Show active menu when url start with menu item url

1.0.5 (2020-8-10)
+++++++++++++++++

* Import FieldDoesNotExist from django.core.exceptions instead django.db.models

1.0.4 (2020-7-31)
+++++++++++++++++

* Import point form gis only one time
* Mark required fields with a *
* Table list set full width by default and hoverable effect

1.0.3 (2020-7-15)
+++++++++++++++++

* Added validation errors below fields in form template
* Fixed problem with import Point

1.0.2 (2020-7-8)
+++++++++++++++++

* Changed sidebar config to support translations
* Added translations

1.0.1 (2020-7-8)
+++++++++++++++++

* Fixed typos
* Fixed extra context in index view

1.0 (2020-6-29)
+++++++++++++++++

* First release on PyPI.
