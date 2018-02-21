from DTrafficControl.settings import IOTA_SEED, IOTA_PROVIDER, MTRAFFIC_REG_TAG
from iota import Iota, BadApiResponse, Transaction, TryteString, Tag, get_current_timestamp, ProposedTransaction, \
    Address, Bundle
import logging
import json
from math import sin, cos, sqrt, atan2, radians

logger = logging.getLogger(__name__)

# approximate radius of earth in km
R = 6373.0


TRAFFIC_STATUS_LEV_3 = "traffic_accident"
TRAFFIC_STATUS_LEV_2 = "traffic_jam"
TRAFFIC_STATUS_LEV_1 = "traffic_alot"
TRAFFIC_STATUS_LEV_0 = "traffic_free"


def get_tags(raw_tag):
    tryte_tag = TryteString(raw_tag[:27])
    tryte_tag += '9' * (27 - len(tryte_tag))
    return Tag(tryte_tag)


def calculate_distance(_lat1, _lon1, _lat2, _lon2):
    """ Return the distance btw two geo locations
    """
    # using haversine formula
    rlat1 = radians(_lat1)
    rlon1 = radians(_lon1)
    rlat2 = radians(_lat2)
    rlon2 = radians(_lon2)

    dlon = rlon2 - rlon1
    dlat = rlat2 - rlat1

    a = sin(dlat / 2) ** 2 + cos(rlat1) * cos(rlat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def is_within_certain_radius(locations, latitude, longitude, radius):
    if locations.get('lat') is None or locations.get('lon') is None:
        return False
    return calculate_distance(locations['lat'], locations['lon'], latitude, longitude) < radius


class IOTAWrapper:

    def __init__(self, seed=IOTA_SEED, node_address=IOTA_PROVIDER):
        self.api = Iota(node_address, seed)

    def get_traffic_status_within(self, radius_in_km, latitude, longitude):
        """ Get traffic status within a radius from longitude and latitude"""
        traffics = []
        if latitude is None or longitude is None:
            return []

        transactions = self._find_transaction()
        if transactions is not None and len(transactions) > 0:
            for tx in transactions:
                if is_within_certain_radius(tx, float(latitude), float(longitude), radius_in_km):
                    traffics.append(tx)

        return traffics

    def broadcast_traffic_status(self, latitude, longitude, traffic_status,
                                 tag=MTRAFFIC_REG_TAG, depth=4, min_weight_magnitude=None):
        logger.info("Broadcast traffic status at lat:{}, lon:{}, status:{}".format(
            latitude,
            longitude,
            traffic_status
        ))
        message = {
            "lat": latitude,
            "lon": longitude,
            "status": traffic_status,
            "timestamp": get_current_timestamp()
        }

        try:
            transfers = [
                # All hail the glory of IOTA and their dummy transactions for tag retrieval. Without multiple
                # transaction, Tangle doesn't seem to pick up our Tag and completely change the value of Tag
                ProposedTransaction(
                    # This address is wholeheartedly irrelevant
                    address=Address("FNAZ9SXUWMPPVHKIWMZWZXSFLPURWIFTUEQCMKGJAKODCMOGCLEAQQQH9BKNZUIFKLOPKRVHDJMBTBFYK"),
                    value=0
                ),
                ProposedTransaction(
                    address=Address("FNAZ9SXUWMPPVHKIWMZWZXSFLPURWIFTUEQCMKGJAKODCMOGCLEAQQQH9BKNZUIFKLOPKRVHDJMBTBFYK"),
                    value=0,
                    tag=get_tags(tag),
                    message=TryteString.from_string(json.dumps(message)),
                )]
            response = self.api.send_transfer(
                depth=depth,
                transfers=transfers,
                min_weight_magnitude=min_weight_magnitude,  # if None, the api will use default number for main-net
            )
        except ConnectionError as e:
            logger.exception("Connection error: {e}".format(e=e))
        except BadApiResponse as e:
            logger.exception("Bad Api Response: {e}".format(e=e))
        except:
            logger.exception("Bad coding")
        else:
            bundle = Bundle(response['bundle'])
            print("Bundle Hash: {}\nFrom Address: {}\nTag:".format(bundle.hash,
                                                                   bundle.transactions[0].address,
                                                                   bundle.transactions[0].tag))
            return response

    def _find_transaction(self, tag=MTRAFFIC_REG_TAG):
        try:
            response = self.api.find_transactions(tags=[get_tags(tag)])
        except ConnectionError as e:
            logger.exception("Connection error: {e}".format(e=e))
        except BadApiResponse as e:
            logger.exception("Bad Api Response: {e}".format(e=e))
        else:
            if len(response["hashes"]) < 1:
                return []
            trytes = self.api.get_trytes(response["hashes"])
            transactions = []
            for trytestring in trytes["trytes"]:
                tx = Transaction.from_tryte_string(trytestring)
                transactions.append(tx)

            return [json.loads(tx.signature_message_fragment.as_string()) for tx in transactions]

