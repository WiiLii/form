pipeline {
	agent {
		any {
			image "mcr.microsoft.com/dotnet/sdk:5.0"
			args "--volume /var/run/docker.sock:/var/run/docker.sock"
		}
	}

	stages {

		stage('Source'){
					steps{
						checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://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@github.com/WiiLii/simple-node-js-react-npm-app.git']]])
					}
				}

		stage('Restore packages'){
           steps{
			   //sh "export PATH=${PATH}:${HOME}/.dotnet"
			   sh 'apt update && apt install -y docker.io'
			   sh 'cd ..'
			   sh 'ls'
               sh 'dotnet restore hacmii/hacmii.sln'
            }
         }

		stage('Clean'){
           steps{
               sh 'dotnet clean hacmii/hacmii.sln --configuration Release'
            }
         }

		stage('Build') {
			environment
			{
				//RSA_KEY = credentials('hacmiiKeys')
				APP_CONFIG_FILE = credentials('App_config')
				DB_SSH_CREDENTIALS = credentials('ict3x03_db_pem')
				TWILIO_APIKEY_FILE = credentials('twilio')
			}
			steps {
				//echo 'building the application'

				sh 'cp "${APP_CONFIG_FILE}" ./hacmii'
				sh 'cp "${DB_SSH_CREDENTIALS}" ./hacmii'
				sh 'cp "${TWILIO_APIKEY_FILE}" ./hacmii'
				sh 'dotnet build hacmii/hacmii.sln --configuration Release --no-restore'
			}
		}

		stage('Automated Testing')
		{
			parallel
			{
				stage('Unit and Integration Tests')
				{
					steps
					{


						sh 'wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
						sh 'apt -y install ./google-chrome-stable_current_amd64.deb'

						sh 'dotnet add hacmii.UnitTests/hacmii.UnitTests.csproj package NunitXml.TestLogger --version 3.0.117'
						sh 'dotnet test hacmii/hacmii.sln --logger:"nunit;logFileName=TestResult.xml"'
						sh 'ls hacmii.UnitTests'
					}
				}

				stage("Owasp Dependency Check"){
					agent {
						docker {
							//
							image "openjdk:17-alpine"
						}
					}
					steps {
							sh 'echo ${JAVA_HOME}'
							dependencyCheck additionalArguments: '--format HTML --format XML', odcInstallation: 'Default'

							dependencyCheckPublisher pattern: 'dependency-check-report.xml'
					}
				}

			}

		}

		stage('Publish NUnit Test Report')
		{
			steps
				{

					//sh 'ls hacmii.UnitTests/TestResults'
					nunit testResultsPattern: 'hacmii.UnitTests/TestResults/TestResults.xml'

				}
		}



		stage('Publish'){
			steps{
				sh 'dotnet publish hacmii/hacmii.csproj --configuration Release --no-restore'
             }
        }

		stage('Deploy'){

			agent none

			steps{
				sh '/usr/local/bin/docker-compose -f ./hacmii/docker-compose.yml down'
				sh '/usr/local/bin/docker-compose -f ./hacmii/docker-compose.yml build'
				sh '/usr/local/bin/docker-compose -f ./hacmii/docker-compose.yml up -d'
             }
		}
	}


}
