# different event triggers

class MetaEventHandler():
    def __init__(self, owner_object, parent = None):
        self.owner_object = owner_object
        self.callback_fns = [] # trigger_event, callback_fn pairs
        self.parent = parent

    def attach_callback(self, trigger_meta_events, callback_fn):
        self.callback_fns.append(
            (trigger_meta_events, callback_fn)
        )
    
    def process_metaevent(self, metaevent):
        print(f"Metaevent Handler of {self.owner_object} received event {metaevent}")

        for triggers, callback in self.callback_fns:
            for trigger in triggers:
                if isinstance(metaevent, trigger):
                    callback(metaevent)
        if self.parent is not None:
            self.parent.process_metaevent(metaevent)

class MetaEvent():
    def __init__(self, trigger_owner):
        self.trigger_owner = trigger_owner

class NAStartME(MetaEvent):
    pass

class NAEndME(MetaEvent):
    pass

class DamageDealt(MetaEvent):
    pass

class DamageReceived(MetaEvent):
    pass

class DidCrit(MetaEvent):
    pass

class SkillME(MetaEvent):
    pass