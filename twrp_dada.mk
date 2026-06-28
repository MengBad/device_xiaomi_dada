# Configure base.mk first to pull in all target binaries/libraries
$(call inherit-product, $(SRC_TARGET_DIR)/product/base.mk)

# Configure core_64_bit_only.mk
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)

# Configure virtual_ab_ota compression
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota/compression_with_xor.mk)

# Configure emulated storage
$(call inherit-product, $(SRC_TARGET_DIR)/product/emulated_storage.mk)

# Inherit from our custom TWRP product configuration
$(call inherit-product, vendor/twrp/config/common.mk)

# Inherit from dada device
$(call inherit-product, device/xiaomi/dada/device.mk)

PRODUCT_DEVICE := dada
PRODUCT_NAME := twrp_dada
PRODUCT_BRAND := Xiaomi
PRODUCT_MODEL := Xiaomi 15
PRODUCT_MANUFACTURER := Xiaomi

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

# Release fingerprint
PRODUCT_BUILD_PROP_OVERRIDES += \
    TARGET_DEVICE="dada" \
    PRODUCT_NAME="dada" \
    PRIVATE_BUILD_DESC="miodm_dada-user 15 AQ3A.250226.002 OS3.0.7.0.WOCCNXM release-keys"

BUILD_FINGERPRINT := Xiaomi/dada/dada:15/AQ3A.250226.002/OS3.0.7.0.WOCCNXM:user/release-keys
