class SyncError(Exception):
    pass


class SourceNotExists(SyncError):
    pass


class DestinationNotExists(SyncError):
    pass
