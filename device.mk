LOCAL_PATH := device/xiaomi/dada

# Enable project path map
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# A/B support
AB_OTA_UPDATER := true

# Dynamic partitions support
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# Override version properties for KeyStore/KeyMint
PRODUCT_SYSTEM_PROPERTIES += \
    ro.build.version.release=15 \
    ro.build.version.release_or_codename=15 \
    ro.build.version.sdk=35
