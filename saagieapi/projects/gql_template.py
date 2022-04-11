#   ___  _ __  __   __ __   __  __ _  _ __  ___
#  / _ \| '_ \ \ \ / / \ \ / / / _` || '__|/ __|
# |  __/| | | | \ V /   \ V / | (_| || |   \__ \
#  \___||_| |_|  \_/     \_/   \__,_||_|   |___/

gql_get_global_env_vars = """
  {
    globalEnvironmentVariables{
      id,
      name,
      scope,
      value,
      description,
      isPassword
    }
  }
  """

gql_create_global_env_var = """
  mutation {{
    saveEnvironmentVariable (
      environmentVariable: {{
        name: "{0}"
        value: "{1}"
        description: "{2}"
        isPassword: {3}
        scope: GLOBAL
      }}
    ) {{
      id
    }}
  }}
"""

gql_delete_env_var = """
  mutation {{
    deleteEnvironmentVariable (
      id: "{0}"
    )
  }}
"""

gql_get_project_env_vars = """
  {{
    projectEnvironmentVariables(projectId: "{0}"){{
      id,
      name,
      scope,
      value,
      description,
      isPassword
    }}
  }}
  """

gql_create_project_env_var = """
  mutation {{
    saveEnvironmentVariable (
      entityId: "{0}"
      environmentVariable: {{
        name: "{1}"
        value: "{2}"
        description: "{3}"
        isPassword: {4}
        scope: PROJECT
      }}
    ) {{
      id
    }}
  }}
"""


#   ____ _           _
#  / ___| |_   _ ___| |_ ___ _ __
# | |   | | | | / __| __/ _ \ '__|
# | |___| | |_| \__ \ ||  __/ |
#  \____|_|\__,_|___/\__\___|_|


gql_get_cluster_info = """
{
  getClusterCapacity {
    cpu
    gpu
    memory
  }
}
"""


#                                 _  _                 _
#  _ __   ___  _ __    ___   ___ (_)| |_   ___   _ __ (_)  ___  ___
# | '__| / _ \| '_ \  / _ \ / __|| || __| / _ \ | '__|| | / _ \/ __|
# | |   |  __/| |_) || (_) |\__ \| || |_ | (_) || |   | ||  __/\__ \
# |_|    \___|| .__/  \___/ |___/|_| \__| \___/ |_|   |_| \___||___/
#             |_|


gql_get_repositories_info = """
  {
    repositories {
      id
      name
      technologies {
        id
        label
        __typename
      }
    }
  }
"""

gql_get_runtimes = """
query technologyQuery($id: UUID!){
    technology(id: $id){ 
        __typename 
        ... on JobTechnology {contexts{label}}
        ... on SparkTechnology {contexts{label}}
        ... on AppTechnology{
            id
            label
            appContexts{
                id
                available
                deprecationDate
                description
                dockerInfo {
                    image
                    version
                }
                facets
                label
                lastUpdate
                ports {
                    basePath
                    name
                    port
                    rewriteUrl
                    scope
                }
                missingFacets
                recommended
                trustLevel
                volumes{
                    path
                    size
                }


            }
        }
    }
}"""

#                        _              _
#  _ __   _ __   ___    (_)  ___   ___ | |_  ___
# | '_ \ | '__| / _ \   | | / _ \ / __|| __|/ __|
# | |_) || |   | (_) |  | ||  __/| (__ | |_ \__ \
# | .__/ |_|    \___/  _/ | \___| \___| \__||___/
# |_|                 |__/


gql_get_projects_info = """
  {
       projects{
          id,
          name,
          creator,
          description,
          jobsCount,
          status
      }
  }
  """

gql_get_project_info = """
  {{
       project(id: "{0}"){{
          name,
          creator,
          description,
          jobsCount,
          status
      }}
  }}
  """

gql_get_project_technologies = """
{{
   project(id: "{0}"){{
   technologiesByCategory {{
      jobCategory,
      technologies{{
        id
        }}
      }}
   }}
}} 
"""

gql_create_project = """
mutation {{
  createProject(project: {{
                    name: "{0}",
                    description: "{1}",
                    {2}
                    technologiesByCategory: [
                      {{
                        jobCategory: "Extraction",
                        technologies: [
                          {3}
                        ]
                      }},
                      {{
                        jobCategory: "Processing",
                        technologies: [
                          {3}
                        ]
                      }}
                    ]
                }}) {{
    id
    name
    creator
  }}
}}
"""

group_block_template = """
authorizedGroups: [
                      {{
                        name: "{0}",
                        role: {1}
                      }}
                    ]
"""

gql_delete_project = """
mutation {{
  archiveProject(
    projectId: "{0}"
  )
}}
"""

#    _         _
#   (_)  ___  | |__   ___
#   | | / _ \ | '_ \ / __|
#   | || (_) || |_) |\__ \
#  _/ | \___/ |_.__/ |___/
# |__/


gql_get_project_jobs = """
  {{
    jobs(projectId: "{0}"){{
      id,
      name,
      description,
      alerting{{
        emails,
        loginEmails{{
          login,
          email
        }},
        statusList
      }},
      countJobInstance,
      instances{1}{{
        id,
        status,
        startTime,
        endTime
      }},
      versions {{
        releaseNote
        runtimeVersion
        commandLine
        isMajor
      }},
      category,
      technology {{
        id
      }},
      isScheduled,
      cronScheduling,
      scheduleStatus,
      isStreaming,
      creationDate,
      migrationStatus,
      migrationProjectId,
      isDeletable,
      pipelines {{
        id
      }}
    }}
  }}
  """

gql_get_project_job = """
  {{
    job(id: "{0}"){{
      id,
      name,
      description,
      alerting{{
        emails,
        loginEmails{{
          login,
          email
        }},
        statusList
      }},
      countJobInstance,
      instances{{
        id,
        status,
        startTime,
        endTime
      }},
      versions {{
        releaseNote
        runtimeVersion
        commandLine
        isMajor
      }},
      category,
      technology {{
        id
      }},
      isScheduled,
      cronScheduling,
      scheduleStatus,
      isStreaming,
      creationDate,
      migrationStatus,
      migrationProjectId,
      isDeletable,
      pipelines {{
        id
      }}
    }}
  }}
  """

gql_get_job_instance = """
  query{{
    jobInstance(id: "{0}"){{
      id,
      status,
      version {{
        releaseNote
        runtimeVersion
        commandLine
        isMajor
        doesUseGPU
      }}
    }}
  }}
  """

gql_run_job = """
  mutation{{
    runJob(jobId: "{0}"){{
      id,
      status
    }}
  }}
  """

gql_stop_job_instance = """
  mutation{{
    stopJobInstance(jobInstanceId: "{0}"){{
      id,
      number,
      status,
      startTime,
      endTime,
      jobId
    }}
  }}
  """

gql_edit_job = """
mutation editJobMutation($id: UUID!, $name: String, $description: String, 
                         $isScheduled: Boolean!, $cronScheduling: Cron, $scheduleTimezone: TimeZone,
                         $alerting: JobPipelineAlertingInput, $resources: JobResourceInput) {
    editJob(job: {
        id: $id
        name: $name
        description: $description
        isScheduled: $isScheduled
        cronScheduling: $cronScheduling
        scheduleTimezone: $scheduleTimezone
        alerting: $alerting
        resources: $resources
    }){
        id
        name
        description
        isScheduled
        cronScheduling
        scheduleTimezone
        resources{
            cpu {
                request
                limit}
            memory{
                request
                limit}
        }
        alerting{
            emails
            statusList
        }
    }
}
"""

gql_create_job = """
mutation createJobMutation($projectId: UUID!, $name: String!, $description: String, $category: String!,
                           $isScheduled: Boolean!, $cronScheduling: Cron, $scheduleTimezone: TimeZone
                           $technologyId: UUID!, 
                           $alerting: JobPipelineAlertingInput, $resources: JobResourceInput,
                           $releaseNote: String, $runtimeVersion: String, $commandLine: String,
                           $dockerInfo: JobDockerInput, $file: Upload) {{
    createJob(job: {{
            projectId: $projectId
            name: $name
            description: $description
            category: $category
            technology: {{
                id: $technologyId
            }}
            isStreaming: false
            isScheduled: $isScheduled
            cronScheduling: $cronScheduling
            scheduleTimezone: $scheduleTimezone
            alerting: $alerting
            resources: $resources
            doesUseGPU: false
        }} 
        jobVersion: {{
            releaseNote: $releaseNote
            runtimeVersion: $runtimeVersion
            commandLine: $commandLine
            {extra_technology}
            dockerInfo: $dockerInfo
        }}
        file: $file){{
        id
        versions {{
            number
            __typename
        }}
        __typename
    }}
}}
"""

gql_upgrade_job = """
mutation addJobVersionMutation($jobId: UUID!, $releaseNote: String, $runtimeVersion: String, $commandLine: String,
                               $usePreviousArtifact: Boolean, $dockerInfo: JobDockerInput, $file: Upload) {{
    addJobVersion(
        jobId: $jobId
        jobVersion: {{
            releaseNote: $releaseNote
            runtimeVersion: $runtimeVersion
            commandLine: $commandLine
            {extra_technology}
            dockerInfo: $dockerInfo
            usePreviousArtifact: $usePreviousArtifact
        }}
        file: $file){{
            number
            __typename
    }}
}}
"""

gql_get_info_job = """query {{
  job(id:"{0}"){{
    id,
    name,
    description,
    creationDate,
    isScheduled,
    cronScheduling,
    scheduleStatus,
    scheduleTimezone,
    isStreaming,
    isDeletable,
    graphPipelines(isCurrent: true){{
      id
    }},
    category,
    technology{{
      id
    }},
    alerting{{
      emails,
      statusList,
      loginEmails{{
        email
      }}
    }},
    resources{{
      cpu{{
        request,
        limit
      }}
      memory{{
        request,
        limit
      }}
    }}
  }}
}}
"""

gql_extra_technology = """
    extraTechnology: {{
        language: "{0}"
        version: "{1}"
    }}"""

gql_delete_job = """
  mutation {{
    archiveJob(
      jobId: "{0}"
    )
  }}
"""

#   __ _  _ __   _ __   ___
#  / _` || '_ \ | '_ \ / __|
# | (_| || |_) || |_) |\__ \
#  \__,_|| .__/ | .__/ |___/
#        |_|    |_|


gql_get_project_apps = """
query labWebAppQuery($id: UUID!){
    labWebApps(projectId: $id){ 
      id
      name
      description
      countJobInstance
      versions {
        number
        creationDate
        releaseNote
        runtimeVersion
        commandLine
        isMajor
        isCurrent
        dockerInfo{
            image
            dockerCredentialsId
        }
        exposedPorts{
            name
            port
            isRewriteUrl
            basePathVariableName
            isAuthenticationRequired
        }
        storagePaths
      }
      category,
      technology {
        id
      }
      alerting {
        emails
        statusList
    }
      creationDate
      isDeletable
      graphPipelines {
        id
      }
      storageSizeInMB
      doesUseGPU
      resources{
        cpu{
          limit
          request
        }
        memory{
          limit
          request
        }
        gpu{
          limit
          request
        }
      }
    }
}
"""

gql_get_project_app = """
query labWebAppQuery($id: UUID!){
    labWebApp(id: $id){ 
      id
      name
      description
      countJobInstance
      versions {
        number
        creationDate
        releaseNote
        runtimeVersion
        commandLine
        isMajor
        isCurrent
        dockerInfo{
            image
            dockerCredentialsId
        }
        exposedPorts{
            name
            port
            isRewriteUrl
            basePathVariableName
            isAuthenticationRequired
        }
        storagePaths
      }
      category,
      technology {
        id
      }
      alerting {
        emails
        statusList
    }
      creationDate
      isDeletable
      graphPipelines {
        id
      }
      storageSizeInMB
      doesUseGPU
      resources{
        cpu{
          limit
          request
        }
        memory{
          limit
          request
        }
        gpu{
          limit
          request
        }
      }
    }
  }
  """

gql_create_app = """
mutation createJobMutation($projectId: UUID!, $name: String!, $description: String, $technologyId: UUID!, 
                           $storageSizeInMB: Int,
                           $image: String!, $dockerCredentialsId: UUID, $exposedPorts: [ExposedPortInput!],
                           $storagePaths: [String!],
                           $releaseNote: String, $alerting: JobPipelineAlertingInput) {
    createJob(job: {
            projectId: $projectId
            name: $name
            description: $description
            category: ""
            technology: {
                id: $technologyId
            }
            isStreaming: false
            isScheduled: false
            storageSizeInMB: $storageSizeInMB
            alerting: $alerting
        }
        jobVersion: {
            dockerInfo: {
                image: $image
                dockerCredentialsId: $dockerCredentialsId
            }
            exposedPorts: $exposedPorts
            storagePaths: $storagePaths 
            releaseNote: $releaseNote
        }){
        id
        versions {
            number
            __typename
        }
        __typename
    }}
"""

gql_edit_app = """
mutation editJobMutation($id: UUID!, $name: String, $description: String, $alerting: JobPipelineAlertingInput) {
    editJob(job: {
        id: $id
        name: $name
        description: $description
        alerting: $alerting
    }){
        id
        name
        description
        creationDate
        technology{
            id
        }
        alerting{
            emails
            statusList
        }
    }
}
"""

#         _               _  _
#  _ __  (_) _ __    ___ | |(_) _ __    ___  ___
# | '_ \ | || '_ \  / _ \| || || '_ \  / _ \/ __|
# | |_) || || |_) ||  __/| || || | | ||  __/\__ \
# | .__/ |_|| .__/  \___||_||_||_| |_| \___||___/
# |_|       |_|

gql_get_pipelines = """
  query{{
    project(id: "{0}"){{
      pipelines{{
        id,
        name,
        description,
        alerting{{
          emails,
          loginEmails{{
            login,
            email
          }},
          statusList
        }},
        pipelineInstanceCount,
        instances{1}{{
          id,
          status,
          startTime,
          endTime
        }},
        creationDate,
        creator,
        isScheduled,
        cronScheduling,
        scheduleStatus,
        scheduleTimezone,
        isLegacyPipeline
      }}
  }}}}
  """

gql_get_pipeline = """
  query{{
    graphPipeline(id: "{0}"){{
      id,
      name,
      description,
      alerting{{
        emails,
        loginEmails{{
          login,
          email
        }},
        statusList
      }},
      pipelineInstanceCount,
      creationDate,
      creator,
      isScheduled,
      cronScheduling,
      scheduleStatus,
      scheduleTimezone,
      isLegacyPipeline
    }}
  }}
  """

gql_stop_pipeline_instance = """
  mutation{{
    stopPipelineInstance(pipelineInstanceId: "{0}"){{
      id,
      number,
      status,
      startTime,
      endTime,
      pipelineId
    }}
  }}
  """

gql_edit_pipeline = """
  mutation($id: UUID!, $name: String, $description: String, $alerting: JobPipelineAlertingInput,
          $isScheduled: Boolean, $cronScheduling: Cron, $scheduleTimezone:TimeZone)  {
    editPipeline(pipeline: {
        id: $id
        name: $name
        description: $description
        alerting:  $alerting
        isScheduled: $isScheduled
        cronScheduling: $cronScheduling
        scheduleTimezone: $scheduleTimezone
      })
    {
      id
      name
      description
      alerting{
        emails
        statusList
      }
      isScheduled
      cronScheduling
      scheduleTimezone
    }
  }
"""

gql_run_pipeline = """
  mutation{{
    runPipeline(pipelineId: "{0}"){{
      id,
      status
    }}
  }}
"""

gql_create_pipeline = """
  mutation {{
      createPipeline(pipeline: {{
          name: "{0}",
          description: "{1}",
          projectId: "{2}",
          jobsId: {3},
          isScheduled: false
      }}){{id}}
  }}
"""

gql_get_pipeline_instance = """
  query {{
      pipelineInstance(id: "{0}"){{
          id,
          status,
          startTime,
          endTime
      }}
  }}
"""

gql_create_graph_pipeline = """
  mutation($jobNodes: [JobNodeInput!], $conditionNodes: [ConditionNodeInput!]) {{
  createGraphPipeline(pipeline:  {{
    name: "{0}",
    description: "{1}",
    projectId: "{2}",
    releaseNote : "{3}",
    {4}
    graph: {{jobNodes: $jobNodes,
                conditionNodes: $conditionNodes}}
    }}
  ) {{
    id
  }}
}}
"""

gql_delete_pipeline = """
  mutation {{
  deletePipeline (
    id: "{0}"
  )
}}
"""

gql_upgrade_pipeline = """
  mutation($id: UUID!, $jobNodes: [JobNodeInput!], $conditionNodes: [ConditionNodeInput!], $releaseNote: String){
  addGraphPipelineVersion(
    pipelineId: $id,
    graph: {jobNodes: $jobNodes,
                conditionNodes: $conditionNodes},
    releaseNote: $releaseNote
    )
    {
      number,
      releaseNote,
      graph{
        jobNodes {
          id,
          job {
            id
          }
        },
        conditionNodes{
          id
        }
      },
      creationDate,
      creator,
      isCurrent,
      isMajor
    }
  }
"""


#
#      _            _                                 _            _   _       _
#     | |          | |                               | |          | | (_)     | |
#   __| | ___   ___| | _____ _ __    ___ _ __ ___  __| | ___ _ __ | |_ _  __ _| |___
#  / _` |/ _ \ / __| |/ / _ \ '__|  / __| '__/ _ \/ _` |/ _ \ '_ \| __| |/ _` | / __|
# | (_| | (_) | (__|   <  __/ |    | (__| | |  __/ (_| |  __/ | | | |_| | (_| | \__ \
#  \__,_|\___/ \___|_|\_\___|_|     \___|_|  \___|\__,_|\___|_| |_|\__|_|\__,_|_|___/
#
#

gql_create_docker_credentials = """
mutation createDockerCredentialsMutation($registry: String, $username: String!, $password: String!, $projectId: UUID!) {
    createDockerCredentials(
        dockerCredentials: {
            registry: $registry
            username: $username
            password: $password 
            projectId: $projectId}){
        id
        registry
        username
        lastUpdate
    }
}
"""

gql_upgrade_docker_credentials = """
mutation updateDockerCredentialsMutation($id: UUID!, $registry: String, $username: String, $password: String!, $projectId: UUID!) {
    updateDockerCredentials(
        dockerCredentialsUpdate: {
            id: $id
            registry: $registry
            username: $username
            password: $password 
            projectId: $projectId}){
        id
        registry
        username
        lastUpdate
    }
}
"""

gql_delete_docker_credentials = """
mutation deleteDockerCredentialsMutation($id: UUID!, $projectId: UUID!) {
    deleteDockerCredentials(
        id: $id
        projectId: $projectId)
}
"""

gql_get_all_docker_credentials = """
query allDockerCredentialsQuery($projectId: UUID!) {
    allDockerCredentials(projectId: $projectId){
        id
        registry
        username
        lastUpdate
        jobs{
            id
        }
    }
}
"""

gql_get_docker_credentials = """
query dockerCredentialsQuery($id: UUID!, $projectId: UUID!) {
    dockerCredentials(id: $id, projectId: $projectId){
        id
        registry
        username
        lastUpdate
        jobs{
            id
        }
    }
}
"""