# -*- mode: ruby -*-
# vi: set ft=ruby ts=4 sw=4 expandtab :

PROJECT = "bbs-app"

PROJECT_DIR="/home/vagrant/black-box-service/"
BUILD_SCRIPTS="#{PROJECT_DIR}/scripts"

# Vagrant port to listen on host
VAGRANT_PORT=ENV.fetch('VAGRANT_PORT', '8001')
# AS port to listen on host
VAGRANT_MOCK_AS_PORT=ENV.fetch('VAGRANT_AS_PORT', '10001')

# S3 port to listen on host
S3_PORT=ENV.fetch('S3_PORT', '5000')
# Kibana port to listen on host
KIBANA_PORT=ENV.fetch('KIBANA_PORT', '5602')

# Vagrant project instance id, 0 by default
VAGRANT_INSTANCE=ENV.fetch('VAGRANT_INSTANCE', '0')

# Vagrant database link (instance id). Create a new DB if empty.
DATABASE_MIGRATION="#{BUILD_SCRIPTS}/provisioning/migrate_database.sh"
S3_MIGRATION="python manage.py collectstatic"
VAGRANT_DB_LINK=ENV.fetch('VAGRANT_DB_LINK', VAGRANT_INSTANCE)
VAGRANT_S3_LINK=ENV.fetch('VAGRANT_S3_LINK', VAGRANT_INSTANCE)
VAGRANT_SQS_LINK=ENV.fetch('VAGRANT_SQS_LINK', VAGRANT_INSTANCE)
VAGRANT_AMS_LINK=ENV.fetch('VAGRANT_AMS_LINK', VAGRANT_INSTANCE)
VAGRANT_ES_LINK=ENV.fetch('VAGRANT_ES_LINK', VAGRANT_INSTANCE)
VAGRANT_AS_LINK=ENV.fetch('VAGRANT_AS_LINK', VAGRANT_INSTANCE)
VAGRANT_US_LINK=ENV.fetch('VAGRANT_US_LINK', VAGRANT_INSTANCE)
VAGRANT_RS_LINK=ENV.fetch('VAGRANT_RS_LINK', VAGRANT_INSTANCE)

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

    # Bucket S3 configuration
    'AWS_ACCESS_KEY_ID': "dummy_value_cannot_be_none",
    'AWS_SECRET_ACCESS_KEY': "dummy_value_cannot_be_none",
    'AWS_S3_HOST': 's3',
    'AWS_S3_PORT': '5000',
    'ADE_AWS_BUK': "mybucket",
    'ADE_STA_URL': 'http://127.0.0.1:5000/%s/',
    'ADE_STA_DOM': '127.0.0.1',
    'ADE_AWS_DIR_STA': 'mybucket',
    'ADE_AWS_DIR_MED': 'mybucket',
    'ADE_BOTO3_ENDPOINT': "http://s3:5000",
    'ADE_STR': 'DEV',

    # SQS (Amazon Simple Queue Service) configuration
    'ADE_BOTO3_SQS_NAME': 'test_android_sqs_name',
    'ADE_BOTO3_SQS_REGION_NAME': "dummy_sqs_region",
    'ADE_BOTO3_SQS_ENDPOINT': 'http://sqs:9324',

    # Elastic search / kibana configuration
    'ES_KIBANA_HOST': 'elasticsearch',

    # virtualenv
    'VIRTUAL_ENV_PATH': '/tmp/virtual_env27',
    'ENV_NAME': 'devdocker',

    'ADE_URL': "http://127.0.0.1:#{VAGRANT_PORT}",
    'ADE_AWS_CDN_DIS': "EGC1V408AFRTK",
    'ADE_DEB': "True",
    'ADE_ALG': "False",
    'ADE_ESB': "False",
    'ADE_ESB_ASS': "False",
    'ADE_ESB_UNA': "False",
    'ADE_ESB_INS': "False",
    'ADE_ESB_UNI': "False",
    'ADE_ESB_URL': "https://qa-esb.aldebaran.com/esb",
    'ADE_JAB': "False",
    'ADE_JAB_TOU': "5",
    'ADE_JAB_ROS': "True",
    'ADE_JAB_MSG': "True",
    'ADE_JAB_SSL': "True",
    'ADE_JAB_DOM': "qa-presence.aldebaran.com",
    'ADE_CAC_BAK': "django.core.cache.backends.locmem.LocMemCache",
    'ADE_CAC_LOC': "unique-snowflake",
    'ADE_MEL_SND': "False",
    'ADE_MEL_PRE': "[ADE Dev]",
    'ADE_MEL_FRM': "[ADE Dev] <no-reply@aldebaran.com>",

    # sso configuration
    'SSO_BASE_URL': "http://127.0.0.1:#{VAGRANT_MOCK_AS_PORT}",
    'SSO_CHECK_REF_BASE_URL': "http://mockas",
    'ADE_PAS_URL': "http://mockas/as/token.oauth2",

    # Policy service configuration
    'AMS_BASE_URL': 'http://ams',

    # User service configuration
    "USER_SERVICE_BASE_URL": "http://user_service",
    "USER_SERVICE_DEPLOYED": 'true',

    # User service settings for testing
    "CLIENT_MOCK_US_HOST": "http://user_service",
    "CLIENT_MOCK_US_PORT": '80',

    # Robot service configuration
    "ROBOT_SERVICE_BASE_URL": "http://robot_service",
    "ROBOT_SERVICE_DEPLOYED": 'true',

    # Robot service settings for testing
    "CLIENT_MOCK_RS_HOST": "http://robot_service",
    "CLIENT_MOCK_RS_PORT": '80',

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

    # Bucket S3 environment
    if (VAGRANT_S3_LINK == VAGRANT_INSTANCE) then
        config.vm.define "s3" do |app|
            app.vm.provider "docker" do |d|
                # Redirect s3 ports so that the content can be accessed from the outside
                d.ports = ["#{S3_PORT}:5000"]
                d.image = "jean553/docker-s3-server-dev"
                d.name = "#{PROJECT}_s3-#{VAGRANT_S3_LINK}"
                d.env = {
                    "S3_BUCKET_NAME" => "mybucket"  # Create the bucket when the container starts
                }
            end
        end
    end

    # mock SQS environment (Amazon Simple Queue Service)
    if (VAGRANT_SQS_LINK == VAGRANT_INSTANCE) then
        config.vm.define "sqs" do |app|
            app.vm.provider "docker" do |d|
                d.image = "behance/elasticmq-docker"
                d.name = "#{PROJECT}_sqs-#{VAGRANT_SQS_LINK}"
            end
        end
    end

    # If a DB is linked we assume that the ams service should be linked too
    if (VAGRANT_AMS_LINK == VAGRANT_INSTANCE) then
        config.vm.define "ams-service" do |app|
            app.vm.provider "docker" do |d|
                d.image = "registry-gitlab.aldebaran.com/microservice/ams"
                d.name = "#{PROJECT}_ams-#{VAGRANT_INSTANCE}"
                d.env = {
                    "AMS_SUPER_USER": "ade_app",
                }
            end
        end
    end

    # If a DB is linked we assume that the elasticsearch service should be linked too
    if (VAGRANT_ES_LINK == VAGRANT_INSTANCE) then
        config.vm.define "elasticsearch" do |app|
            app.vm.provider "docker" do |d|
                d.image = "nshou/elasticsearch-kibana"
                d.name = "#{PROJECT}_elasticsearch-#{VAGRANT_INSTANCE}"
                d.ports = ["#{KIBANA_PORT}:5601"]
            end
        end
    end

    # User Service API
    if (VAGRANT_US_LINK == VAGRANT_INSTANCE) then
        config.vm.define "mock-user-service-api" do |app|
            app.vm.provider "docker" do |d|
                d.image = "registry-gitlab.aldebaran.com/mocks/mock_user_service"
                d.name = "#{PROJECT}_mock_user_service-#{VAGRANT_US_LINK}"
            end
        end
    end

    # Robot Service API
    if (VAGRANT_RS_LINK == VAGRANT_INSTANCE) then
        config.vm.define "mock-robot-service-api" do |app|
            app.vm.provider "docker" do |d|
                d.image = "registry-gitlab.aldebaran.com/mocks/mock_robot_service"
                d.name = "#{PROJECT}_mock_robot_service-#{VAGRANT_RS_LINK}"
            end
        end
    end

    # AS Mock
    if (VAGRANT_AS_LINK == VAGRANT_INSTANCE) then
        config.vm.define "mock-authorization-server" do |app|
            app.vm.provider "docker" do |d|
                d.image = "registry-gitlab.aldebaran.com/mocks/mock_authorization_server"
                d.name = "#{PROJECT}_mock_as-#{VAGRANT_AS_LINK}"
                d.ports = ["#{VAGRANT_MOCK_AS_PORT}:80"]
                d.env = {
                    "MOCK_AS_CALLBACK_SSO_URL" => "http://127.0.0.1:#{VAGRANT_PORT}/callback_sso",
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
            d.link "#{PROJECT}_s3-#{VAGRANT_S3_LINK}:s3"
            d.link "#{PROJECT}_sqs-#{VAGRANT_SQS_LINK}:sqs"
            d.link "#{PROJECT}_ams-#{VAGRANT_AMS_LINK}:ams"
            d.link "#{PROJECT}_mock_as-#{VAGRANT_AS_LINK}:mockas"
            d.link "#{PROJECT}_elasticsearch-#{VAGRANT_ES_LINK}:elasticsearch"
            d.link "#{PROJECT}_mock_user_service-#{VAGRANT_US_LINK}:user_service"
            d.link "#{PROJECT}_mock_robot_service-#{VAGRANT_RS_LINK}:robot_service"
            d.volumes =  [
                "#{ENV['PWD']}/:#{PROJECT_DIR}"
            ]
            d.env = DOCKER_ENV
            d.has_ssh = true
        end

        # so that we can git clone from within the docker
        app.vm.provision "file", source: "~/.ssh/id_rsa", destination: ".ssh/id_rsa"
        # so that we can git push from inside the docker
        app.vm.provision "file", source: "~/.gitconfig", destination: ".gitconfig"

        # we can't copy in /root using file provisionner
        # hence the usage of shell
        app.vm.provision "permits-root-to-clone", type: "shell" do |s|
            s.inline = "cp /home/vagrant/.ssh/id_rsa ~/.ssh/id_rsa"
        end

        # Note: we're using a shell to launch ansible
        # instead of directly using the `ansible_local` because of this
        # http://stackoverflow.com/questions/37989742
        app.vm.provision "local_ansible", type: "shell" do |s|
            s.env = DOCKER_ENV
            s.inline = "
                set -e
                cd $APP_PATH
                # we add aldebaran's gitlab to known hosts, otherwise ansible will fail
                # to clone the roles
                ssh-keyscan -H gitlab.aldebaran.com >> $HOME/.ssh/known_hosts
                ansible-galaxy install -r build_scripts/ansible/requirements.yml
                ansible-playbook build_scripts/ansible/bootstrap-dev.yml
            "
        end

        app.vm.provision :shell, :inline => <<-END
            set -e
            ZSHRC=/home/vagrant/.zshrc

            # Usefull aliases
            echo 'alias adeStart="python manage.py runserver 0.0.0.0:8000"' >>  $ZSHRC
            echo 'alias adeURLExport="export ADE_URL=http://127.0.0.1:8000"' >>  $ZSHRC
            echo 'alias adeFuncTestStart="python manage.py adetestf --domain=http://127.0.0.1:8000"' >>  $ZSHRC

            #{DATABASE_MIGRATION}

            echo "done, you can now run 'vagrant ssh '"
        END

        app.ssh.username = "vagrant"
        app.ssh.password = ""
    end
end
