from whitenoise import storage


class CompressedManifestStaticFilesStorage(storage.CompressedManifestStaticFilesStorage):
    def make_helpful_exception(self, exception, name):
        return True  # :trollface:  # Ignore the exception and continue processing other files