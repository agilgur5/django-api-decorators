# changelog-maker only gets name from package.json, so do a replace
npx @agilgur5/changelog-maker | sed 's_nodejs/node_agilgur5/django-api-decorators_';
