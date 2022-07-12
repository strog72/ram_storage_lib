# ram_storage_lib
Ф library that allows you to save the value by key.
It should use a single storage in RAM, it should, by the values of the system variable, periodically reset the snapshot of the storage to the file system.
It should, by the value of the system variable, periodically overwrite the storage from the modified one 
(that is, periodically request a snapshot and update the storage if it has been changed) snapshot from the file system. 
