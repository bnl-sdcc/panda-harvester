from pandaharvester.harvestercore import core_utils
from pandaharvester.harvestercore.work_spec import WorkSpec
from pandaharvester.harvestercore.plugin_base import PluginBase

from pandaharvester.harvestersubmitter.apfgrid_submitter import APFGridSubmitter



# setup base logger
baseLogger = core_utils.setup_logger()

# dummy monitor
class APFGridMonitor(PluginBase):
    # constructor
    def __init__(self, **kwarg):
        PluginBase.__init__(self, **kwarg)
        self.log = core_utils.make_logger(baseLogger)
              
        
        self.log.debug('APFGridMonitor initialized.')
        
        
        

    # check workers
    def check_workers(self, workspec_list):
        """Check status of workers. This method takes a list of WorkSpecs as input argument
        and returns a list of worker's statuses.
        Nth element if the return list corresponds to the status of Nth WorkSpec in the given list. Worker's
        status is one of WorkSpec.ST_finished, WorkSpec.ST_failed, WorkSpec.ST_cancelled, WorkSpec.ST_running,
        WorkSpec.ST_submitted.

        :param workspec_list: a list of work specs instances
        :return: A tuple of return code (True for success, False otherwise) and a list of worker's statuses.
        :rtype: (bool, [string,])
        """
        current = APFGridSubmitter.workers
        self.log.debug("%s workers in current status %s workers in workspec_list" % (len(current), len(workspec_list)))
        retlist = []
        for workSpec in workspec_list:
            self.log.debug("Worker(workerId=%s queueName=%s computingSite=%s status=%s )" % (workSpec.workerID, 
                                                                               workSpec.queueName,
                                                                               workSpec.computingSite, 
                                                                               workSpec.status) )
            newStatus = WorkSpec.ST_submitted
            found = False
            for worker in current:
                if worker.workerID == workSpec.workerID:
                    self.log.debug("Found matching worker: %s with ID %s" % (worker, worker.workerID))
                    found = True
                    retlist.append((worker.status, ''))
            if not found:
                retlist.append((newStatus, ''))
        self.log.debug('retlist=%s' % retlist)
        return True, retlist

    