# -*- mode: ruby -*-
# vi: set ft=ruby ts=4 sw=4 expandtab :

PROJECT = "BBX-app"

PROJECT_DIR="/home/vagrant/black-box-service"
BUILD_SCRIPTS="#{PROJECT_DIR}/scripts"

# Vagrant port to listen on host*
VAGRANT_PORT=ENV.fetch('VAGRANT_PORT', '8001')

# Vagrant project instance id, 0 by default
VAGRANT_INSTANCE=ENV.fetch('VAGRANT_INSTANCE', '0')

# Vagrant database link (instance id). Create a new DB if empty.
DATABASE_MIGRATION="#{BUILD_SCRIPTS}/provisioning/migrate_database.sh"
S3_MIGRATION="python manage.py collectstatic"
VAGRANT_DB_LINK=ENV.fetch('VAGRANT_DB_LINK', VAGRANT_INSTANCE)

if VAGRANT_DB_LINK != VAGRANT_INSTANCE
    # We won't execute database migration if the DB is linked
    DATABASE_MIGRATION = ""
end
UID = Process.euid

DOCKER_ENV = {
    # for ansible
    "TARGET" => "dev",

    # database configuration
    'ADE_BDD_ENG': 'django.db.backends.mysql',
    'ADE_BDD_SVR': 'db',
    'ADE_BDD_USR': 'vagrant',
    'ADE_BDD_NAM': 'vagrant',
    'ADE_BDD_PWD': 'vagrant',
    # For provisioning
    'MYSQL_ROOT_PASSWORD': 'vagrant',

    'JWT_VERIFY': 'False',

    'APP_NAME': PROJECT,
    'APP_PATH': PROJECT_DIR,

    # virtualenv
    'VIRTUAL_ENV_PATH': '/tmp/virtual_env35',
    'ENV_NAME': 'devdocker3',

    'ADE_URL': "http://127.0.0.1:#{VAGRANT_PORT}",
    'ADE_DEB': "True",
    'ADE_ALG': "False",
    'ADE_CAC_BAK': "django.core.cache.backends.locmem.LocMemCache",
    'ADE_CAC_LOC': "unique-snowflake",
    'ADE_MEL_SND': "False",
    'ADE_MEL_PRE': "[ADE Dev]",

    'HOST_USER_UID': UID,
    'DB_HOST': "db",
    'PROJECT_DIR': PROJECT_DIR,
}

ENV['VAGRANT_NO_PARALLEL'] = 'yes'
ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
Vagrant.configure(2) do |config|

    config.ssh.forward_agent = true

    # If no DB_LINK found in the environment start a new one
    if (VAGRANT_DB_LINK == VAGRANT_INSTANCE) then
        config.vm.define "db" do |app|
            app.vm.provider "docker" do |d|
                d.image = "mysql:5.6"
                d.name = "#{PROJECT}_db-#{VAGRANT_DB_LINK}"
                d.env = {
                  "MYSQL_ROOT_PASSWORD" => "vagrant",
                  "MYSQL_DATABASE" => "vagrant",
                  "MYSQL_USER" => "vagrant",
                  "MYSQL_PASSWORD" => "vagrant",
                }
            end
        end
    end


    config.vm.define "dev", primary: true do |app|
        app.vm.provider "docker" do |d|
            # Django server listening on 8000, redirect on VAGRANT_PORT on host
            d.ports = ["#{VAGRANT_PORT}:8000"]

            d.image = "allansimon/allan-docker-dev-python"
            d.name = "#{PROJECT}_dev-#{VAGRANT_INSTANCE}"
            d.link "#{PROJECT}_db-#{VAGRANT_DB_LINK}:db"
            d.volumes =  [
                "#{ENV['PWD']}/:#{PROJECT_DIR}"
            ]
            d.env = DOCKER_ENV
            d.has_ssh = true
        end

        # Note: we're using a shell to launch ansible
        # instead of directly using the `ansible_local` because of this
        # http://stackoverflow.com/questions/37989742
        app.vm.provision "local_ansible", type: "shell" do |s|
            s.env = DOCKER_ENV
            s.inline = "
                set -e
                cd $APP_PATH
                ansible-playbook build_scripts/ansible/bootstrap-dev.yml
            "
        end

        app.vm.provision :shell, :inline => <<-END
        set -e
        ZSHRC=/home/vagrant/.zshrc

        # Usefull aliases
        echo 'alias adeStart="python manage.py runserver 0.0.0.0:8000"' >>  $ZSHRC

        #{DATABASE_MIGRATION}

        echo "done, you can now run 'vagrant ssh '"

        END

        app.ssh.username = "vagrant"
        app.ssh.password = ""
    end
end
