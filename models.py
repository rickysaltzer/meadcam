# Mead fermentation class, which will act as a model
# for storing data and persisting it into HBase.

import happybase
import datetime
import time
import base64
from hashlib import md5


class HBaseConnection(object):
    """
    This holds a persistent connection to an HBase table and
    can be passed around to models to be used as a medium
    of connection
    """

    def __init__(self, host, table, autoconnect=False):
        self.__connection = happybase.Connection(host, autoconnect=autoconnect, compat="0.92")
        self.__connection.open()

        try:
            self.__table = self.__connection.table(table)
        except:
            raise NameError("Table Does Not Exist [%s]" % (self.table))

    @property
    def connection(self):
        return self.__connection

    @property
    def table(self):
        return self.__table


class MeadModel(object):
    """
    This acts as a database model, it holds some specified
    values and then will persist those values into HBase
    using the HBaseConnection class
    """

    def __init__(self, brew_id, rms, height, width, image, connection):
        """
        Mead Model constructor, accepts the following
        brew_id     | ID number of thise brewcam
                      this will be used for the key
        rms         | The calculated RMS value
        height      | Image height
        width       | Image width
        image       | PIL image buffer
        connection  | HBaseConnection class to use for transport
        """
        self.brew_id = brew_id
        self.time = time.time()
        self.date = datetime.datetime.fromtimestamp(self.time)
        self.rms = str(rms)
        self.height = str(height)
        self.width = str(width)
        self.image = image
        self.connection = connection

    @property
    def key(self):
        return "|".join([md5(self.brew_id).hexdigest(), str(self.time)])

    def save(self):
        """
        Saves the image to HBase
        # Column Family: meta
            - brew id
            - epoch time
            - rms
        # Column Family: raw
            - image height
            - image width
            - b64 encoded image
        """
        table = self.connection.table
        table.put(self.key, {
            'meta:brew_id': self.brew_id,
            'meta:time': str(self.time),
            'meta:rms': self.rms,
            'raw:height': self.height,
            'raw:width': self.width,
            'raw:image': base64.b64encode(self.image.tostring())
        })
