import h5py

from lyse import Run

import numpy as np

class Shot(Run):  
    def get_spcm_counts(self):
            """
            Gets the spcm counts from the shot and stores it in results. 
            
            The spcm returns a cumulative count every time it is triggered. 
            Every time we want to count, we send a pair of triggers, one at the 
            start and one at the end. 
            Therefore we want to calculate the difference between the readings at 
            the first and second trigger, third and fourth trigger, etc.
            
            Note that this method doesn't return anything. The resulting counts can
            be accessed as self.spcm_single_count for shots with one count (i.e.
            two triggers), or self.spcm_multi_counts for shots with more than one
            counts. The counting intervals can be similarly accessed as 
            self.spcm_single_interval or self.spcm_multi_intervals. 
            
            Tested to work for shots with one count. 
            Need to test for shots with more than two triggers. 

            Args:
                none
            
            Beili 01/04/23
            """

            


            # Retrieve the spcm data
            with h5py.File(self.h5_path,'r') as f:
                spcm_trigger_times = f['data/traces/spcm_counts/spcm_counts']['t']
                spcm_values = f['data/traces/spcm_counts/spcm_counts']['values']

            # Store raw cumulative counter samples as attributes
            self.spcm_trigger_times = spcm_trigger_times
            self.spcm_values = spcm_values

            # Defaults, so these always exist
            self.spcm_counts = np.array([], dtype=np.int64)
            self.spcm_intervals = np.array([], dtype=np.float64)

            
            # Check that the spcm values and times have the same nonzero length
            if len(spcm_values) != len(spcm_trigger_times):
                message = (f"Received '{len(spcm_trigger_times)}' triggers"
                        "but '{len(spcm_value)}' values.")
                raise ValueError(message)
            elif len(spcm_values) == 0:
                message = (f"Received '{len(spcm_values)}' spcm values.")
                raise ValueError(message)
            elif len(spcm_values) %2 != 0:
                message = (f"Received '{len(spcm_values)}' spcm values."
                        "Expected an even number.")
                raise ValueError(message)
            
            else:
                self.save_result('spcm_num', len(spcm_values)/2)
                # If there are only two triggers, save as a number
                if len(spcm_values) == 2:
                    self.save_result('spcm_single_count', spcm_values[1]-spcm_values[0])
                    self.save_result('spcm_single_interval', spcm_trigger_times[1]-spcm_trigger_times[0])

                    self.spcm_counts = spcm_counts
                    self.spcm_intervals = spcm_intervals

                    self.save_result('spcm_single_count', spcm_counts[0])
                    self.save_result('spcm_single_interval', spcm_intervals[0])

                    self.save_result_array('spcm_counts', spcm_counts)
                    self.save_result_array('spcm_intervals', spcm_intervals)

                elif len(spcm_values) == 4:
                    
                    self.save_result('spcm_single_count', spcm_values[3]-spcm_values[2])
                    self.save_result('spcm_single_interval', spcm_trigger_times[3]-spcm_trigger_times[2])


                    self.spcm_counts = spcm_counts
                    self.spcm_intervals = spcm_intervals

                    self.save_result('spcm_num', 1)
                    self.save_result('spcm_single_count', spcm_counts[0])
                    self.save_result('spcm_single_interval', spcm_intervals[0])

                    self.save_result_array('spcm_counts', spcm_counts)
                    self.save_result_array('spcm_intervals', spcm_intervals)

                # If there are more than two triggers, save the difference between 1-2,
                # 3-4, etc. into arrays
                else:
                    spcm_counts = spcm_values[1::2] - spcm_values[0::2]
                    spcm_intervals = spcm_trigger_times[1::2] - spcm_trigger_times[0::2]

                    self.spcm_counts = spcm_counts
                    self.spcm_intervals = spcm_intervals


                    self.save_result_array('spcm_multi_counts', spcm_counts)
                    self.save_result_array('spcm_multi_intervals', spcm_intervals)

                    self.save_result_array('spcm_counts', spcm_counts)
                    self.save_result_array('spcm_intervals', spcm_intervals)


