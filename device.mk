LOCAL_PATH := device/xiaomi/dada

# Enable project path map
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH)

# A/B support
AB_OTA_UPDATER := true

# Dynamic partitions support
PRODUCT_USE_DYNAMIC_PARTITIONS := true
