import saga

from pandaharvester.harvestercore import core_utils
from pandaharvester.harvestercore.plugin_base import PluginBase
from pandaharvester.harvestersubmitter.saga_submitter import SAGASubmitter

# logger
baseLogger = core_utils.setup_logger('saga_monitor')


# monitor through SAGA
class SAGAMonitor(PluginBase):
    # constructor
    def __init__(self, **kwarg):
        PluginBase.__init__(self, **kwarg)
        tmpLog = core_utils.make_logger(baseLogger, method_name='__init__')
        tmpLog.info("[{0}] SAGA adaptor will be used".format(self.adaptor))

    # check workers
    def check_workers(self, workspec_list):
        """Check status of workers. This method takes a list of WorkSpecs as input argument
        and returns a list of worker's statuses.
  
        :param workspec_list: a list of work specs instances
        :return: A tuple of return code (True for success, False otherwise) and a list of worker's statuses.
        :rtype: (bool, [string,])
        """
        job_service = saga.job.Service(self.adaptor)

        retList = []
        for workSpec in workspec_list:
            # make logger
            errStr = ''
            tmpLog = core_utils.make_logger(baseLogger, 'workerID={0}'.format(workSpec.workerID),
                                            method_name='check_workers')
            if workSpec.batchID:
                saga_submission_id = '[{0}]-[{1}]'.format(self.adaptor, workSpec.batchID)
                try:
                    worker = job_service.get_job(saga_submission_id)
                    tmpLog.info('SAGA State for submission with batchid: {0} is: {1}'.format(workSpec.batchID, worker.state))
                    harvester_job_state = SAGASubmitter.status_translator(worker.state)
                    tmpLog.info(
                        'Worker state with batchid: {0} is: {1}'.format(workSpec.batchID, harvester_job_state))

                except saga.SagaException as ex:
                    tmpLog.error('An exception occured during retriving worker information')
                    errStr = ex.get_message()
                    # probably 'failed' is not proper state in this case, 'undefined' looks a bit better
                    harvester_job_state = workSpec.ST_failed 
                retList.append((harvester_job_state, errStr))

        job_service.close()

        return True, retList
