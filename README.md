HOW TO HIGHLIGHT
# recipe-app-api
`The template string highlight`


16-1 vid
Recipe API Project

Model => serializer => viewset => in urls.py file

<!-- CREATE SUPER USER -->

docker compose run --rm app sh -c "python manage.py createsuperuser"

docker compose -f docker-compose-avi.yml run --rm app sh -c "python manage.py makemigrations"

docker compose -f docker-compose-avi.yml up --build

read dictionary / object cannot use dot notation
name = data.get('name')
name = data['name']













































---------------------------------------------------------------

# if we link one id to the model of another table we use foreign key

# if we link many id in a field and send it like an array of ids we use manytomany

we can give string name of the model or the import of the whole model
tags = models.ManyToManyField('Tag')
OR
assignees = models.ManyToManyField(mAuthMod.CustomUser,
                                    related_name='assignees_projects',
                                    blank=True)







---------------------------------------------------------------

`New stuff`

 extra_kwargs = {'image': {'required': 'True'}}, it is used in the serializer
