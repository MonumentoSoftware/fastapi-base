ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)


build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

enter:
	docker-compose exec $(ARG) bash


ne-routine:
	python sigmine_script_routine.py