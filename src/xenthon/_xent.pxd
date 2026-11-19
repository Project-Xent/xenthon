from libc.stddef cimport wchar_t
from libc.stdint cimport uint8_t, uint32_t, int32_t, uint64_t


cdef extern from "xtk/xtk_scene.h" nogil:
    ctypedef uint64_t XtkCtrl
    ctypedef uint64_t XtkResource
    ctypedef uint32_t XtkCtrlId
    ctypedef uint32_t XtkPropertyId
    ctypedef uint32_t XtkEventId
    ctypedef uint32_t XtkLocalId
    ctypedef uint32_t XtkSubRef
    ctypedef uint64_t XtkSubId
    ctypedef uint64_t XtkSourceId

    ctypedef struct XtkColor:
        uint32_t rgba

    ctypedef struct XtkChangeStamp:
        XtkSourceId source
        uint64_t revision

    ctypedef union XtkNodeRefU:
        XtkCtrl existing
        XtkLocalId local

    ctypedef struct XtkNodeRef:
        int kind
        XtkNodeRefU u

    ctypedef struct XtkValueString:
        char *data
        uint32_t len

    ctypedef struct XtkValueBytes:
        uint8_t *data
        uint32_t len

    ctypedef union XtkValueU:
        bint b
        int32_t i32
        float f32
        double f64
        uint32_t u32
        XtkColor color
        XtkValueString string
        XtkResource resource
        XtkValueBytes bytes

    ctypedef struct XtkValue:
        int kind
        XtkValueU u

    ctypedef struct XtkPropPatch:
        XtkPropertyId id
        XtkValue value
        XtkChangeStamp change

    ctypedef struct XtkPayloadString:
        const char *data
        uint32_t len

    ctypedef struct XtkPayloadQuery:
        const char *text
        uint32_t len
        int32_t index

    ctypedef struct XtkPayloadRating:
        double value
        int32_t count

    ctypedef struct XtkPayloadIndexBool:
        int32_t index
        bint value

    ctypedef struct XtkPayloadRange:
        float start
        float end

    ctypedef struct XtkPayloadWindow:
        int32_t first
        int32_t last
        int32_t lanes

    ctypedef struct XtkPayloadScroll:
        float x
        float y
        float max_x
        float max_y

    ctypedef union XtkEventPayloadU:
        bint b
        int32_t i32
        float f32
        double f64
        XtkPayloadString string
        XtkPayloadQuery query
        XtkPayloadRating rating
        XtkPayloadIndexBool index_bool
        XtkPayloadRange range
        XtkPayloadWindow window
        XtkPayloadScroll scroll

    ctypedef struct XtkEventPayload:
        int kind
        XtkEventPayloadU u

    ctypedef struct XtkEvent:
        XtkEventId id
        XtkCtrl source
        XtkCtrl target
        XtkCtrl current_target
        int phase
        int cause
        uint64_t scene_revision
        XtkChangeStamp change
        XtkEventPayload payload

    ctypedef uint32_t (*XtkEventFn)(void *arg, const XtkEvent *event) noexcept

    ctypedef struct XtkHost:
        pass

    ctypedef struct XtkBatch:
        pass

    ctypedef struct XtkScene:
        XtkHost *host

    ctypedef struct XtkTxn:
        XtkScene *scene
        XtkBatch *batch
        bint borrowed

    ctypedef struct XtkControlMapping:
        XtkLocalId local
        XtkCtrl control

    ctypedef struct XtkSubMapping:
        XtkSubRef token
        XtkSubId id

    ctypedef struct XtkBatchResult:
        XtkControlMapping *controls
        uint32_t control_count
        XtkSubMapping *subscriptions
        uint32_t subscription_count

    ctypedef struct XtkBatchDiag:
        int error
        uint32_t failed_op
        int stage

    enum:
        XTK_REF_NONE
        XTK_REF_EXISTING
        XTK_REF_LOCAL
        XTK_VALUE_BOOL
        XTK_VALUE_I32
        XTK_VALUE_F32
        XTK_VALUE_F64
        XTK_VALUE_ENUM
        XTK_VALUE_COLOR
        XTK_VALUE_STRING
        XTK_VALUE_RESOURCE
        XTK_VALUE_BYTES
        XTK_EVENT_PHASE_MASK_TARGET
        XTK_EVENT_CONTINUE
        XTK_EVENT_HANDLED
        XTK_EVENT_CAUSE_USER
        XTK_EVENT_PAYLOAD_NONE
        XTK_EVENT_PAYLOAD_BOOL
        XTK_EVENT_PAYLOAD_I32
        XTK_EVENT_PAYLOAD_F32
        XTK_EVENT_PAYLOAD_F64
        XTK_EVENT_PAYLOAD_STRING
        XTK_EVENT_PAYLOAD_QUERY
        XTK_EVENT_PAYLOAD_RATING
        XTK_EVENT_PAYLOAD_INDEX_BOOL
        XTK_EVENT_PAYLOAD_RANGE
        XTK_EVENT_PAYLOAD_WINDOW
        XTK_EVENT_PAYLOAD_SCROLL
        XTK_MIRROR_MAX

    XtkScene xtk_scene_fromhost(XtkHost *host)
    XtkCtrl xtk_scene_root(const XtkScene *scene)
    bint xtk_txn_begin(XtkScene *scene, XtkTxn *out)
    XtkBatchResult *xtk_txn_commit(XtkTxn *txn, XtkBatchDiag *diagnostic)
    void xtk_txn_abort(XtkTxn *txn)
    XtkLocalId xtk_txn_create(XtkTxn *txn, XtkCtrlId type, XtkNodeRef parent, XtkNodeRef before,
                              const XtkPropPatch *props, uint32_t prop_count)
    bint xtk_txn_drop(XtkTxn *txn, XtkNodeRef target)
    bint xtk_txn_set(XtkTxn *txn, XtkNodeRef target, XtkPropertyId id, XtkValue value, XtkChangeStamp change)
    bint xtk_txn_move(XtkTxn *txn, XtkNodeRef parent, XtkNodeRef child, XtkNodeRef before)
    XtkSubRef xtk_txn_on(XtkTxn *txn, XtkNodeRef target, XtkEventId event, uint32_t phases, XtkEventFn fn, void *arg)
    bint xtk_txn_off(XtkTxn *txn, XtkSubId id)
    void xtk_batchresult_destroy(XtkBatchResult *result)


cdef extern from "xtk/xtk_catalog.h" nogil:
    uint32_t xtk_catalog_mirrors(XtkCtrlId control, XtkEventId event, XtkPropertyId *out)


cdef extern from "fluxent/flux_app.h" nogil:
    ctypedef struct FluxApp:
        pass

    ctypedef struct FluxAppCfg:
        const wchar_t *title
        int width
        int height
        int theme
        int backdrop
        void *on_start
        void *on_stop
        void *user

    enum:
        FLUX_BACKDROP_MICA
        FLUX_THEME_SYSTEM
        FLUX_THEME_LIGHT
        FLUX_THEME_DARK

    FluxApp *flux_app_create(const FluxAppCfg *cfg)
    void flux_app_destroy(FluxApp *app)
    int flux_app_run(FluxApp *app)
    void flux_app_redraw(FluxApp *app)
    void flux_app_onframe(FluxApp *app, void (*cb)(void *ctx) noexcept, void *ctx)
    bint flux_app_invoke(FluxApp *app, void (*fn)(void *ctx) noexcept nogil, void *ctx)
    bint flux_app_setfocus(FluxApp *app, XtkCtrl control)


cdef extern from "fluxent/flux_host.h" nogil:
    XtkHost *flux_app_attachhost(FluxApp *app)
    void flux_host_destroy(XtkHost *host)


cdef extern from "fluxent/flux_controls.h" nogil:
    void flux_controls_all()
